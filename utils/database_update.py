# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import gzip
import logging
import time
from datetime import UTC, datetime, timedelta
from random import randint
from typing import Literal, TypeVar
from urllib.parse import unquote, unquote_plus
from xml.etree import ElementTree

import requests
from django.conf import settings
from django.db import transaction
from django.db.models import Count, F
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, Timeout
from urllib3.util import Retry

import metrics
from base.models import Outline, Player, Tribe, VillageModel, World
from tribal_wars_planer.settings import fanout_cache

log = logging.getLogger(__name__)

MAX_LAST_MODIFIED_EXISTING = 14
MAX_LAST_MODIFIED_NEW = 3
STATUS_200 = 200

retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
global_adapter = HTTPAdapter(max_retries=retry_strategy)


class DatabaseUpdateError(Exception):
    pass


class WorldOutdatedError(DatabaseUpdateError):
    pass


# Helper function to safely get and convert XML values
T = TypeVar("T", int, float, str)


def get_xml_value(parent: ElementTree.Element, tag: str, convert_type: type[T]) -> T:
    element = parent.find(tag)
    if element is None:
        raise DatabaseUpdateError(f"Missing required XML tag: {tag}")
    if element.text is None:
        raise DatabaseUpdateError(f"Empty value for XML tag: {tag}")
    try:
        return convert_type(element.text)
    except ValueError:
        raise DatabaseUpdateError(f"Invalid value for {tag}: {element.text}")


class WorldUpdateHandler:
    VILLAGE_DATA: Literal["/map/village.txt.gz"] = "/map/village.txt.gz"
    TRIBE_DATA: Literal["/map/ally.txt.gz"] = "/map/ally.txt.gz"
    PLAYER_DATA: Literal["/map/player.txt.gz"] = "/map/player.txt.gz"
    DATA_TYPES = Literal[
        "/map/village.txt.gz", "/map/ally.txt.gz", "/map/player.txt.gz"
    ]

    def __init__(self, world: World) -> None:
        self.deleted: bool = False
        self.world = world
        self.player_log_msg: str | None = None
        self.tribe_log_msg: str | None = None
        self.village_log_msg: str | None = None

    def create_or_update_config(self) -> None:
        try:
            with requests.Session() as session:
                session.mount("https://", global_adapter)
                req = session.get(
                    self.world.link_to_game("/interface.php?func=get_config"),
                    timeout=3.05,
                )
        except (Timeout, ConnectionError) as e:
            raise DatabaseUpdateError(f"Connection error: {str(e)}")

        if req.history:
            raise DatabaseUpdateError("Request was redirected")

        if req.status_code != STATUS_200:
            raise DatabaseUpdateError(f"Invalid status code: {req.status_code}")

        try:
            tree = ElementTree.fromstring(req.content)
        except ElementTree.ParseError as e:
            raise DatabaseUpdateError(f"Failed to parse XML: {str(e)}")

        # Get main config values
        speed_world = get_xml_value(tree, "speed", float)
        speed_units = get_xml_value(tree, "unit_speed", float)
        morale = get_xml_value(tree, "moral", int)

        # Get game section values
        game_tag = tree.find("game")
        if game_tag is None:
            raise DatabaseUpdateError("Missing game section in XML")

        paladin = get_xml_value(game_tag, "knight", int)
        archer = get_xml_value(game_tag, "archer", int)

        # Get nobleman section values
        nobleman_tag = tree.find("snob")
        if nobleman_tag is None:
            raise DatabaseUpdateError("Missing snob section in XML")

        max_noble_distance = get_xml_value(nobleman_tag, "max_dist", int)

        # Update world object
        self.world.speed_world = speed_world
        self.world.speed_units = speed_units
        self.world.morale = morale
        self.world.paladin = "active" if bool(paladin) else "inactive"
        self.world.archer = "active" if bool(archer) else "inactive"
        self.world.max_noble_distance = max_noble_distance

        # Get unit info
        try:
            with requests.Session() as session:
                session.mount("https://", global_adapter)
                req_units = session.get(
                    self.world.link_to_game("/interface.php?func=get_unit_info"),
                    timeout=3.05,
                )
        except (Timeout, ConnectionError) as e:
            raise DatabaseUpdateError(f"Connection error getting unit info: {str(e)}")

        if req_units.history:
            raise DatabaseUpdateError("Unit info request was redirected")
        if req_units.status_code != STATUS_200:
            raise DatabaseUpdateError(
                f"Invalid status code for unit info: {req_units.status_code}"
            )

        try:
            tree_units = ElementTree.fromstring(req_units.content)
        except ElementTree.ParseError as e:
            raise DatabaseUpdateError(f"Failed to parse unit info XML: {str(e)}")

        militia_found = any(child.tag == "militia" for child in tree_units)
        self.world.militia = "active" if militia_found else "inactive"

        # Check village data availability
        try:
            with requests.Session() as session:
                session.mount("https://", global_adapter)
                req_data = session.get(
                    self.world.link_to_game(self.VILLAGE_DATA),
                    stream=True,
                    timeout=3.05,
                )
                req_data.close()

        except (Timeout, ConnectionError) as e:
            raise DatabaseUpdateError(
                f"Connection error checking village data: {str(e)}"
            )

        if req_data.history:
            raise DatabaseUpdateError("Village data request was redirected")
        if req_data.status_code != STATUS_200:
            raise DatabaseUpdateError(
                f"Invalid status code for village data: {req_data.status_code}"
            )

        # Check last modified date
        try:
            last_modified = WorldUpdateHandler.last_modified(
                req_data.headers["last-modified"]
            )
        except (KeyError, ValueError) as e:
            raise DatabaseUpdateError(f"Invalid last-modified header: {str(e)}")

        now = datetime.now(UTC)
        if last_modified < now - timedelta(days=MAX_LAST_MODIFIED_NEW):
            raise WorldOutdatedError(
                f"World data too old: last modified is {last_modified}, "
                f"which is over {MAX_LAST_MODIFIED_NEW} days old"
            )

        self.world.save()

    @staticmethod
    def delete_world(world: World) -> bool:
        log.warning("Start delete of world %s", world)
        outline_count = Outline.objects.filter(world=world).count()
        if outline_count:
            log.warning(
                "Could not delete world %s, there are still %s related outlines",
                world,
                outline_count,
            )
            world.pending_delete = True
            world.save()
            return False
        else:
            world.delete()
            try:
                metrics.WORLD_LAST_UPDATE.labels(world=str(world)).set(0)
            except Exception as err:
                log.error(
                    "Could not clear metric WORLD_LAST_UPDATE for %s: %s",
                    world,
                    err,
                    exc_info=True,
                )

            log.info("Deleted world %s", world)
            return True

    def check_if_world_is_archived(self, url_param: str) -> None:
        log.info("Checking world archive of url %s", url_param)
        postfix = str(self.world)
        if f"/archive/{postfix}" in url_param:
            log.warning("World %s flagged as archived, trying to delete it", self.world)
            self.deleted = self.delete_world(self.world)
        else:
            log.warning(
                "World %s does not look like archived, connection error?", self.world
            )
            self.handle_connection_error()

    def handle_connection_error(self) -> None:
        msg = f"conn error {self.world.link_to_game()}"
        metrics.ERRORS.labels(msg).inc()
        World.objects.filter(pk=self.world.pk).update(
            connection_errors=F("connection_errors") + 1
        )

    @staticmethod
    def last_modified(datetime_string: str) -> datetime:
        """Converts 'Sun, 08 May 2022 06:15:20 GMT' to datetime"""
        last_modified_datetime = datetime.strptime(
            datetime_string, "%a, %d %b %Y %H:%M:%S %Z"
        )
        last_modified_datetime = last_modified_datetime.replace(tzinfo=UTC)
        return last_modified_datetime

    def update_all(self, download_try: int = settings.WORLD_UPDATE_TRY_COUNT) -> str:
        """Synchronize Tribe, Village, Player tables with latest data from game."""
        count = 0
        log.info("%s start download_and_save data from tribal wars", self.world)
        while count < download_try:
            self.download_and_save(self.PLAYER_DATA)
            time.sleep(0.2 + randint(1, 20) / 60)
            self.download_and_save(self.VILLAGE_DATA)
            time.sleep(0.2 + randint(1, 20) / 60)
            self.download_and_save(self.TRIBE_DATA)
            count += 1
            if count < download_try:
                time.sleep(0.5 + randint(1, 20) / 60)

        if self.deleted or self.world.pending_delete:
            return f"{self.world} was deleted or is going to be deleted"

        log.info("%s start atomic transaction", self.world)
        with transaction.atomic():
            tribe_cache_key = self.get_latest_data_key(self.TRIBE_DATA)
            log.info("%s tribe_cache_key is %s", self.world, tribe_cache_key)
            if tribe_cache_key != self.world.fanout_key_text_tribe:
                tribe_text = fanout_cache.get(tribe_cache_key, retry=True)
                self.world.fanout_key_text_tribe = tribe_cache_key
                self.update_tribes(text=tribe_text)  # type: ignore
            log.info("%s finish update_tribes", self.world)

            player_cache_key = self.get_latest_data_key(self.PLAYER_DATA)
            log.info("%s player_cache_key is %s", self.world, player_cache_key)
            if player_cache_key != self.world.fanout_key_text_player:
                player_text = fanout_cache.get(player_cache_key, retry=True)
                self.world.fanout_key_text_player = player_cache_key
                self.update_players(text=player_text)  # type: ignore
            log.info("%s finish update_players", self.world)

            village_cache_key = self.get_latest_data_key(self.VILLAGE_DATA)
            log.info("%s village_cache_key is %s", self.world, village_cache_key)
            if village_cache_key != self.world.fanout_key_text_village:
                village_text = fanout_cache.get(village_cache_key, retry=True)
                self.world.fanout_key_text_village = village_cache_key
                self.update_villages(text=village_text)  # type: ignore
            log.info("%s finish update_villages", self.world)

            message = (
                f"{self.world} | tribe_updated: {self.tribe_log_msg} |"
                f" village_update: {self.tribe_log_msg} |"
                f" player_update: {self.tribe_log_msg}"
            )
            self.world.save(
                update_fields=[
                    "fanout_key_text_tribe",
                    "fanout_key_text_player",
                    "fanout_key_text_village",
                    "updated_at",
                ]
            )

        return message

    def download_and_save(self, data_type: "WorldUpdateHandler.DATA_TYPES") -> None:
        """Download data (NOT ALWAYS latest) from game API in text format and save in disk cache"""
        if self.deleted:
            return
        log.info("%s download_and_save: %s", self.world, data_type)
        with requests.Session() as session:
            session.mount("https://", global_adapter)
            try:
                res = session.get(
                    self.world.link_to_game(data_type),
                    stream=True,
                    timeout=3.05,
                )
                if res.history:
                    log.warning(
                        "World %s got redirect when requested %s",
                        self.world,
                        self.world.link_to_game(data_type),
                    )
                    res.close()
                    return self.check_if_world_is_archived(res.url)
                if res.status_code != STATUS_200:
                    log.error(
                        "%s download_and_save: %s: unexpected status code %d",
                        self.world,
                        data_type,
                        res.status_code,
                    )
                    res.close()
                    return self.handle_connection_error()
                # handle last-modified header without accessing body
                last_modified = WorldUpdateHandler.last_modified(
                    res.headers["last-modified"]
                )
                now = datetime.now(UTC)
                if last_modified < now - timedelta(days=MAX_LAST_MODIFIED_EXISTING):
                    log.warning(
                        "world %s: last modified is %s that is over %dd old",
                        self.world,
                        last_modified,
                        MAX_LAST_MODIFIED_EXISTING,
                    )
                    res.close()
                    self.deleted = self.delete_world(self.world)
                    return

                unique_cache_key = (
                    f"{self.world}_{data_type}_{last_modified.timestamp()}"
                )
                if unique_cache_key in fanout_cache:
                    res.close()
                    return
                # only now make another request to get body
                text = gzip.decompress(res.content).decode()
                res.close()
                log.info(f"setting cache key {unique_cache_key}")
                fanout_cache.set(unique_cache_key, text, expire=3 * 60 * 60, retry=True)

            except (Timeout, ConnectionError) as err:
                log.error(err, exc_info=True)
                self.handle_connection_error()

    def get_latest_data_key(self, data_type: "WorldUpdateHandler.DATA_TYPES") -> str:
        """Get latest key (by 'last-modified' datetime) from disk cache"""
        cache_key_prefix = f"{self.world}_{data_type}_"
        result_list: list[str] = []
        for key in fanout_cache:
            if str(key).startswith(cache_key_prefix):
                result_list.append(str(key))

        result_list.sort(reverse=True)
        return result_list[0]

    def update_villages(self, text: str) -> None:
        create_list: list[VillageModel] = []

        players = Player.objects.filter(world=self.world)
        player_ids_map: dict[int, Player] = {
            player.player_id: player for player in players
        }

        duplicated_ids_list: list[str] = list(
            VillageModel.objects.filter(world=self.world)
            .values_list("village_id", flat=True)
            .annotate(num_id=Count("village_id"))
            .filter(num_id__gt=1)
        )
        if duplicated_ids_list:
            VillageModel.objects.filter(
                world=self.world, village_id__in=duplicated_ids_list
            ).delete()

        villages_barbarian: set[tuple[int, int, int]] = set(
            VillageModel.objects.filter(player=None, world=self.world).values_list(
                "village_id", "x_coord", "y_coord"
            )
        )
        villages_humans: set[tuple[int, int, int, int]] = set(
            VillageModel.objects.select_related()
            .exclude(player=None)
            .filter(world=self.world)
            .values_list("village_id", "player__player_id", "x_coord", "y_coord")
        )

        for line in [i.split(",") for i in text.split("\n")]:
            if line == [""]:
                continue

            village_id = int(line[0])
            player_id = int(line[4])
            x = int(line[2])
            y = int(line[3])

            if (village_id, x, y) in villages_barbarian and player_id == 0:
                villages_barbarian.remove((village_id, x, y))
                continue

            if (village_id, player_id, x, y) in villages_humans:
                villages_humans.remove((village_id, player_id, x, y))
                continue

            if player_id == 0:
                player = None
            elif player_id not in player_ids_map:
                continue
            else:
                player = player_ids_map[player_id]

            village = VillageModel(
                village_id=village_id,
                x_coord=x,
                y_coord=y,
                coord=f"{x}|{y}",
                player=player,
                world=self.world,
            )
            create_list.append(village)

        village_ids_to_remove = [int(village[0]) for village in villages_barbarian] + [
            int(village[0]) for village in villages_humans
        ]

        VillageModel.objects.filter(
            village_id__in=village_ids_to_remove, world=self.world
        ).delete()
        VillageModel.objects.bulk_create(create_list)
        metrics.DBUPDATE.labels("village", self.world.postfix, "create").inc(
            len(create_list)
        )
        metrics.DBUPDATE.labels("village", self.world.postfix, "delete").inc(
            len(village_ids_to_remove)
        )
        self.village_log_msg = f"C-{len(create_list)},D-{len(village_ids_to_remove)}"

    def update_tribes(self, text: str) -> None:
        create_list: list[Tribe] = []

        tribe_set: set[tuple[int, str]] = set(
            Tribe.objects.filter(world=self.world).values_list("tribe_id", "tag")
        )

        for line in [i.split(",") for i in text.split("\n")]:
            if line == [""]:
                continue

            tribe_id = int(line[0])
            tag = unquote(unquote_plus(line[2]))

            if (tribe_id, tag) in tribe_set:
                tribe_set.remove((tribe_id, tag))

            else:
                tribe = Tribe(tribe_id=tribe_id, tag=tag, world=self.world)
                create_list.append(tribe)

        Tribe.objects.filter(
            tribe_id__in=[item[0] for item in tribe_set], world=self.world
        ).delete()
        Tribe.objects.bulk_create(create_list)
        metrics.DBUPDATE.labels("tribe", self.world.postfix, "create").inc(
            len(create_list)
        )
        metrics.DBUPDATE.labels("tribe", self.world.postfix, "delete").inc(
            len(tribe_set)
        )
        self.tribe_log_msg = f"C-{len(create_list)},D-{len(tribe_set)}"

    def update_players(self, text: str) -> None:
        create_list: list[Player] = []
        update_list: list[Player] = []

        players = Player.objects.filter(world=self.world)
        player_ids_map: dict[int, Player] = {
            player.player_id: player for player in players
        }

        tribes = Tribe.objects.filter(world=self.world)
        tribe_context: dict[int, Tribe] = {tribe.tribe_id: tribe for tribe in tribes}

        players_without_tribe: set[tuple[int, str, int, int]] = set(
            Player.objects.filter(tribe=None, world=self.world).values_list(
                "player_id", "name", "villages", "points"
            )
        )

        players_with_tribe: set[tuple[int, str, int, int, int]] = set(
            Player.objects.exclude(tribe=None)
            .filter(world=self.world)
            .select_related("tribe")
            .values_list("player_id", "name", "tribe__tribe_id", "villages", "points")
        )

        for line in [i.split(",") for i in text.split("\n")]:
            if line == [""]:
                continue

            player_id = int(line[0])
            name = unquote(unquote_plus(line[1]))
            tribe_id = int(line[2])
            villages = int(line[3])
            points = int(line[4])

            if (
                player_id,
                name,
                villages,
                points,
            ) in players_without_tribe and tribe_id == 0:
                players_without_tribe.remove((player_id, name, villages, points))
                del player_ids_map[player_id]
                continue

            if (player_id, name, tribe_id, villages, points) in players_with_tribe:
                players_with_tribe.remove((player_id, name, tribe_id, villages, points))
                del player_ids_map[player_id]
                continue

            # else create or update
            if tribe_id == 0:
                tribe = None
            elif tribe_id not in tribe_context:
                continue
            else:
                tribe = tribe_context[tribe_id]

            if player_id in player_ids_map:
                player = player_ids_map[player_id]
                player.name = name
                player.tribe = tribe
                player.villages = villages
                player.points = points
                update_list.append(player)
                del player_ids_map[player_id]
            else:
                player = Player(
                    player_id=player_id,
                    name=name,
                    tribe=tribe,
                    world=self.world,
                    villages=villages,
                    points=points,
                )
                create_list.append(player)

        Player.objects.bulk_update(update_list, ["name", "tribe", "points", "villages"])
        Player.objects.filter(
            world=self.world, player_id__in=player_ids_map.keys()
        ).delete()
        Player.objects.bulk_create(create_list)
        metrics.DBUPDATE.labels("player", self.world.postfix, "create").inc(
            len(create_list)
        )
        metrics.DBUPDATE.labels("player", self.world.postfix, "delete").inc(
            len(player_ids_map)
        )
        metrics.DBUPDATE.labels("player", self.world.postfix, "update").inc(
            len(update_list)
        )
        self.player_log_msg = (
            f"C-{len(create_list)},D-{len(player_ids_map)},U-{len(update_list)}"
        )
