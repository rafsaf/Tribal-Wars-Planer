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
from urllib.parse import unquote, unquote_plus
from xml.etree import ElementTree

import requests
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from base.models import Player, Tribe, VillageModel, World


def cron_schedule_data_update():
    """Update all Tribe, VillageModel, Player instances"""
    worlds = []
    for world in World.objects.select_related("server").exclude(postfix="Test"):
        instance = WorldQuery(world=world)
        instance.update_all()
        worlds.append(world)
        logging.info(
            f"{str(world)} | tribe_updated: {instance.tribe_update} |"
            f" village_update: {instance.village_update} |"
            f" player_update: {instance.player_update}"
        )
    World.objects.bulk_update(
        worlds, ["last_update", "etag_player", "etag_tribe", "etag_village"]
    )


class WorldQuery:
    def __init__(self, world: World):
        self.world = world
        self.player_update: bool = False
        self.tribe_update: bool = False
        self.village_update: bool = False

    def check_if_world_exist_and_try_create(self) -> tuple[World | None, str]:
        """
        Check if world exists in game
        if world is already added, return tuple None, 'added'
        if yes, return tuple World instance, 'success'
        if no, return tuple None, 'error'
        """
        if World.objects.filter(
            server=self.world.server, postfix=self.world.postfix
        ).exists():
            return (None, "added")
        try:
            req = requests.get(
                self.world.link_to_game("/interface.php?func=get_config")
            )
        except requests.exceptions.RequestException:
            return (None, "error")
        if req.history:
            return (None, "error")
        if req.status_code != 200:
            return (None, "error")

        tree = ElementTree.fromstring(req.content)
        self.world.speed_world = float(tree[0].text)  # type: ignore
        self.world.speed_units = float(tree[1].text)  # type: ignore
        if bool(int(tree[7][1].text)):  # type: ignore
            self.world.paladin = "active"
        else:
            self.world.paladin = "inactive"

        if bool(int(tree[7][3].text)):  # type: ignore
            self.world.archer = "active"
        else:
            self.world.archer = "inactive"

        self.world.max_noble_distance = int(tree[9][3].text)  # type: ignore

        try:
            req_units = requests.get(
                self.world.link_to_game("/interface.php?func=get_unit_info")
            )
        except requests.exceptions.RequestException:
            return (None, "error")
        if req_units.history:
            return (None, "error")
        if req_units.status_code != 200:
            return (None, "error")

        tree_units = ElementTree.fromstring(req_units.content)

        militia_found = False
        for child in tree_units:
            if child.tag == "militia":
                militia_found = True
                break

        if militia_found:
            self.world.militia = "active"
        else:
            self.world.militia = "inactive"

        self.world.save()
        return (self.world, "success")

    def check_if_world_is_archived(self, url_param: str):
        postfix = str(self.world)
        archive_end = f"/archive/{postfix}"
        if url_param.endswith(archive_end):
            self.world.delete()
        else:
            self.handle_connection_error()

    def handle_connection_error(self):
        self.world.connection_errors += 1
        self.world.save()

    def update_all(self):
        self.update_tribes()
        self.update_players()
        self.update_villages()
        self.world.last_update = timezone.now()

    def update_villages(self):
        dupl_ids = list(
            VillageModel.objects.filter(world=self.world)
            .values_list("village_id", flat=True)
            .annotate(num_id=Count("village_id"))
            .filter(num_id__gt=1)
        )
        if len(dupl_ids) > 0:
            VillageModel.objects.filter(
                world=self.world, village_id__in=dupl_ids
            ).delete()

        create_list = list()

        try:
            req = requests.get(
                self.world.link_to_game("/map/village.txt.gz"), stream=True
            )
        except requests.exceptions.RequestException:
            self.handle_connection_error()

        else:
            if req.history:
                return self.check_if_world_is_archived(req.url)
            elif req.headers["etag"] == self.world.etag_village:
                return
            else:
                text = gzip.decompress(req.content).decode()
                self.world.etag_village = req.headers["etag"]
                self.village_update = True
            player_context = {}

            players = Player.objects.filter(world=self.world)
            for player in players:
                player_context[player.player_id] = player

            village_set1 = set(
                VillageModel.objects.filter(player=None, world=self.world).values_list(
                    "village_id", "x_coord", "y_coord"
                )
            )
            village_set2 = set(
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

                if (village_id, x, y) in village_set1 and player_id == 0:
                    village_set1.remove((village_id, x, y))
                    continue

                if (village_id, player_id, x, y) in village_set2:
                    village_set2.remove((village_id, player_id, x, y))
                    continue

                if player_id == 0:
                    player = None
                elif player_id not in player_context:
                    continue
                else:
                    player = player_context[player_id]

                village = VillageModel(
                    village_id=village_id,
                    x_coord=x,
                    y_coord=y,
                    coord=f"{x}|{y}",
                    player=player,
                    world=self.world,
                )
                create_list.append(village)

            village_ids_to_remove = [int(village[0]) for village in village_set1] + [
                int(village[0]) for village in village_set2
            ]
            with transaction.atomic():
                VillageModel.objects.filter(
                    village_id__in=village_ids_to_remove, world=self.world
                ).delete()
                VillageModel.objects.bulk_create(create_list)

    def update_tribes(self):
        create_list = list()

        try:
            req = requests.get(self.world.link_to_game("/map/ally.txt.gz"), stream=True)
        except requests.exceptions.RequestException:
            self.handle_connection_error()

        else:
            if req.history:
                return self.check_if_world_is_archived(req.url)
            elif req.headers["etag"] == self.world.etag_tribe:
                return
            else:
                text = gzip.decompress(req.content).decode()
                self.world.etag_tribe = req.headers["etag"]
                self.tribe_update = True
            tribe_set = set(
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
            with transaction.atomic():
                Tribe.objects.filter(
                    tribe_id__in=[item[0] for item in tribe_set], world=self.world
                ).delete()
                Tribe.objects.bulk_create(create_list)

    def update_players(self):
        create_list = list()

        try:
            req = requests.get(
                self.world.link_to_game("/map/player.txt.gz"), stream=True
            )
        except requests.exceptions.RequestException:
            self.handle_connection_error()

        else:
            if req.history:
                return self.check_if_world_is_archived(req.url)
            elif req.headers["etag"] == self.world.etag_player:
                return
            else:
                text = gzip.decompress(req.content).decode()
                self.world.etag_player = req.headers["etag"]
                self.player_update = True
            tribe_context = {}

            tribes = Tribe.objects.filter(world=self.world)
            for tribe in tribes:
                tribe_context[tribe.tribe_id] = tribe

            player_set1 = set(
                Player.objects.filter(tribe=None, world=self.world).values_list(
                    "player_id", "name", "villages", "points"
                )
            )

            player_set2 = set(
                Player.objects.exclude(tribe=None)
                .filter(world=self.world)
                .select_related("tribe")
                .filter(world=self.world)
                .values_list(
                    "player_id", "name", "tribe__tribe_id", "villages", "points"
                )
            )

            for line in [i.split(",") for i in text.split("\n")]:
                if line == [""]:
                    continue

                player_id = int(line[0])
                name = unquote(unquote_plus(line[1]))
                tribe_id = int(line[2])
                villages = int(line[3])
                points = int(line[4])

                if (player_id, name, villages, points) in player_set1 and tribe_id == 0:
                    player_set1.remove((player_id, name, villages, points))
                    continue

                if (player_id, name, tribe_id, villages, points) in player_set2:
                    player_set2.remove((player_id, name, tribe_id, villages, points))
                    continue

                # else create
                if tribe_id == 0:
                    tribe = None
                elif tribe_id not in tribe_context:
                    continue
                else:
                    tribe = tribe_context[tribe_id]

                player = Player(
                    player_id=player_id,
                    name=name,
                    tribe=tribe,
                    world=self.world,
                    villages=villages,
                    points=points,
                )
                create_list.append(player)

            players_ids_to_remove = [player[0] for player in player_set1] + [
                player[0] for player in player_set2
            ]
            with transaction.atomic():
                Player.objects.filter(
                    world=self.world, player_id__in=players_ids_to_remove
                ).delete()
                Player.objects.bulk_create(create_list)
