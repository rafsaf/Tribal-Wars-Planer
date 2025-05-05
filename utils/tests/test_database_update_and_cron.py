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

from pathlib import Path
from unittest.mock import patch

import pytest
import requests
import requests_mock
from diskcache import FanoutCache
from freezegun import freeze_time

from base.models import Player, Tribe, VillageModel, World
from base.tests.test_utils.mini_setup import MiniSetup
from tribal_wars_planer import settings as tw_settings
from utils import database_update
from utils.database_update import WorldUpdateHandler


@pytest.fixture(autouse=True)
def mock_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Clear the disk cache"""
    path = tmp_path / "cache"
    path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(
        tw_settings,
        "fanout_cache",
        FanoutCache(directory=path, timeout=1, shards=2, size_limit=1 * 2**30),
    )


CURRENT_DIRECTORY = Path(__file__).parent
GET_CONFIG = (CURRENT_DIRECTORY / "database_update/get_config.xml").read_text()
GET_CONFIG_2 = (CURRENT_DIRECTORY / "database_update/get_config_2.xml").read_text()
GET_UNIT_INFO = (CURRENT_DIRECTORY / "database_update/get_unit_info.xml").read_text()
GET_UNIT_INFO_2 = (
    CURRENT_DIRECTORY / "database_update/get_unit_info_2.xml"
).read_text()
TRIBES = (CURRENT_DIRECTORY / "database_update/ally.txt.gz").read_bytes()
PLAYERS = (CURRENT_DIRECTORY / "database_update/player.txt.gz").read_bytes()
VILLAGES = (CURRENT_DIRECTORY / "database_update/village.txt.gz").read_bytes()
TRIBES_UPDATED = (
    CURRENT_DIRECTORY / "database_update/ally_updated.txt.gz"
).read_bytes()
PLAYERS_UPDATED = (
    CURRENT_DIRECTORY / "database_update/player_updated.txt.gz"
).read_bytes()
VILLAGES_UPDATED = (
    CURRENT_DIRECTORY / "database_update/village_updated.txt.gz"
).read_bytes()


class WorldUpdateHandlerTest(MiniSetup):
    def setUp(self) -> None:
        super().setUp()
        self.world = self.get_world(save=False)

    def test_connection_error_get_config(self) -> None:
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"),
                exc=requests.exceptions.ConnectionError,
            )
            with self.assertRaises(database_update.DatabaseUpdateError):
                world_query.create_or_update_config()

    def test_connection_bad_status_get_config(self) -> None:
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"), status_code=400
            )
            with self.assertRaises(database_update.DatabaseUpdateError):
                world_query.create_or_update_config()

    def test_connection_redirect_get_config(self) -> None:
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"),
                [
                    {
                        "text": GET_CONFIG,
                        "status_code": 300,
                    },
                    {
                        "text": GET_CONFIG,
                        "status_code": 200,
                    },
                ],
            )
            with self.assertRaises(database_update.DatabaseUpdateError):
                world_query.create_or_update_config()

    def test_connection_error_get_unit_info(self) -> None:
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"),
                [
                    {
                        "text": GET_CONFIG,
                        "status_code": 200,
                    }
                ],
            )
            mock.get(
                world.link_to_game("/interface.php?func=get_unit_info"),
                exc=requests.exceptions.ConnectionError,
            )
            with self.assertRaises(database_update.DatabaseUpdateError):
                world_query.create_or_update_config()

    def test_connection_bad_status_get_unit_info(self) -> None:
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"),
                [
                    {
                        "text": GET_CONFIG,
                        "status_code": 200,
                    }
                ],
            )
            mock.get(
                world.link_to_game("/interface.php?func=get_unit_info"),
                [
                    {
                        "text": GET_UNIT_INFO,
                        "status_code": 404,
                    }
                ],
            )
            with self.assertRaises(database_update.DatabaseUpdateError):
                world_query.create_or_update_config()

    def test_connection_redirect_get_unit_info(self) -> None:
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"),
                [
                    {
                        "text": GET_CONFIG,
                        "status_code": 200,
                    }
                ],
            )
            mock.get(
                world.link_to_game("/interface.php?func=get_unit_info"),
                [
                    {
                        "text": GET_UNIT_INFO,
                        "status_code": 300,
                    },
                    {
                        "text": GET_UNIT_INFO,
                        "status_code": 200,
                    },
                ],
            )
            with self.assertRaises(database_update.DatabaseUpdateError):
                world_query.create_or_update_config()

    @freeze_time("2022-05-08 07:00:00")
    def test_create_or_update_config(self) -> None:
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        assert world_query.world.paladin == "inactive"
        assert world_query.world.archer == "inactive"
        assert world_query.world.militia == "inactive"
        with requests_mock.Mocker() as mock:
            mock.get(
                self.world.link_to_game("/interface.php?func=get_config"),
                [
                    {
                        "text": GET_CONFIG,
                        "status_code": 200,
                    },
                ],
            )
            mock.get(
                self.world.link_to_game("/interface.php?func=get_unit_info"),
                [
                    {
                        "text": GET_UNIT_INFO,
                        "status_code": 200,
                    },
                ],
            )
            mock.get(
                world_query.world.link_to_game("/map/village.txt.gz"),
                content=VILLAGES,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            world_query.create_or_update_config()

        world_query.world.refresh_from_db()
        assert world_query.world.speed_world == 1.6
        assert world_query.world.speed_units == 0.625
        assert world_query.world.paladin == "active"
        assert world_query.world.archer == "active"
        assert world_query.world.militia == "active"
        assert world_query.world.morale == 1
        assert world_query.world.max_noble_distance == 100
        assert world_query.world.fanout_key_text_player == "__0"
        assert world_query.world.fanout_key_text_tribe == "__0"
        assert world_query.world.fanout_key_text_village == "__0"

    @freeze_time("2022-05-08 07:00:00")
    def test_create_or_update_config_case2(self) -> None:
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        assert world_query.world.paladin == "inactive"
        assert world_query.world.archer == "inactive"
        assert world_query.world.militia == "inactive"
        with requests_mock.Mocker() as mock:
            mock.get(
                self.world.link_to_game("/interface.php?func=get_config"),
                [
                    {
                        "text": GET_CONFIG_2,
                        "status_code": 200,
                    },
                ],
            )
            mock.get(
                self.world.link_to_game("/interface.php?func=get_unit_info"),
                [
                    {
                        "text": GET_UNIT_INFO_2,
                        "status_code": 200,
                    },
                ],
            )
            mock.get(
                world_query.world.link_to_game("/map/village.txt.gz"),
                content=VILLAGES,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            world_query.create_or_update_config()

        world_query.world.refresh_from_db()
        assert world_query.world.speed_world == 4.0
        assert world_query.world.speed_units == 0.5
        assert world_query.world.paladin == "active"
        assert world_query.world.archer == "inactive"
        assert world_query.world.militia == "inactive"
        assert world_query.world.morale == 2
        assert world_query.world.max_noble_distance == 500
        assert world_query.world.fanout_key_text_player == "__0"
        assert world_query.world.fanout_key_text_tribe == "__0"
        assert world_query.world.fanout_key_text_village == "__0"

    @freeze_time("2022-05-11 07:00:00")
    def test_create_or_update_config_wont_create_old_world(self) -> None:
        world_query = WorldUpdateHandler(world=self.world)
        with requests_mock.Mocker() as mock:
            mock.get(
                self.world.link_to_game("/interface.php?func=get_config"),
                [
                    {
                        "text": GET_CONFIG,
                        "status_code": 200,
                    },
                ],
            )
            mock.get(
                self.world.link_to_game("/interface.php?func=get_unit_info"),
                [
                    {
                        "text": GET_UNIT_INFO,
                        "status_code": 200,
                    },
                ],
            )
            mock.get(
                world_query.world.link_to_game("/map/village.txt.gz"),
                content=VILLAGES,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            with self.assertRaises(database_update.DatabaseUpdateError):
                world_query.create_or_update_config()
        assert World.objects.all().count() == 0

    def test_if_world_if_archived1(self) -> None:
        world = self.world
        world.save()
        world.refresh_from_db()
        world_query = WorldUpdateHandler(world=world)
        world_query.check_if_world_is_archived("https://example.com/archive/nt1")
        assert not World.objects.filter(pk=world.pk).exists()

    def test_if_world_if_archived2(self) -> None:
        world = self.world
        world.save()
        world.refresh_from_db()
        world_query = WorldUpdateHandler(world=world)
        world_query.check_if_world_is_archived("https://example.com/archive/nope")
        assert World.objects.filter(pk=world.pk).exists()
        world_query.world.refresh_from_db()
        assert world_query.world.connection_errors == 1

    def test_last_modified(self) -> None:
        datetime = "Sat, 08 Jan 2022 13:48:44 GMT"
        assert WorldUpdateHandler.last_modified(datetime).timestamp() == 1641649724

    @freeze_time("2022-05-08 07:00:00")
    @patch("time.sleep", return_value=None)
    def test_db_update_cron_job(self, patched_time_sleep) -> None:
        self.world.save()

        with requests_mock.Mocker() as mock:
            world_query = WorldUpdateHandler(world=self.world)
            mock.get(
                world_query.world.link_to_game("/map/player.txt.gz"),
                content=PLAYERS,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            mock.get(
                world_query.world.link_to_game("/map/ally.txt.gz"),
                content=TRIBES,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            mock.get(
                world_query.world.link_to_game("/map/village.txt.gz"),
                content=VILLAGES,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            world_query.update_all()
            self.world.refresh_from_db()
            date1 = self.world.updated_at
            assert VillageModel.objects.count() == 38219
            assert Player.objects.count() == 10234
            assert Tribe.objects.count() == 534
            with freeze_time("2022-05-08 07:00:01"):
                world_query.update_all()
                self.world.refresh_from_db()
                assert VillageModel.objects.count() == 38219
                assert Player.objects.count() == 10234
                assert Tribe.objects.count() == 534
                date2 = self.world.updated_at
                assert date2 > date1
            assert (
                self.world.fanout_key_text_player
                == "nt1_/map/player.txt.gz_1651990520.0"
            )
            assert (
                self.world.fanout_key_text_tribe == "nt1_/map/ally.txt.gz_1651990520.0"
            )
            assert (
                self.world.fanout_key_text_village
                == "nt1_/map/village.txt.gz_1651990520.0"
            )
            tribe_1 = Tribe.objects.get(tribe_id=30)
            assert tribe_1.world == self.world
            assert tribe_1.tag == "BNAB"
            tribe_2 = Tribe.objects.get(tribe_id=35)
            assert tribe_2.world == self.world
            assert tribe_2.tag == "BG"
            assert not Tribe.objects.filter(tribe_id=2000).exists()
            assert Tribe.objects.filter(tribe_id=1826).exists()

            player_1 = Player.objects.get(player_id=11480)
            assert player_1.name == "Nakon"
            assert player_1.world.pk == self.world.pk
            assert player_1.villages == 0
            assert player_1.points == 0
            assert player_1.tribe is not None
            assert player_1.tribe.tribe_id == 1097
            player_2 = Player.objects.get(player_id=39848)
            assert player_2.name == "polakumie"
            assert player_2.world.pk == self.world.pk
            assert player_2.villages == 21
            assert player_2.points == 217132
            assert player_2.tribe is not None
            assert player_2.tribe.tribe_id == 67
            player_3 = Player.objects.get(player_id=17714)
            assert player_3.name == "skobol"
            assert player_3.world.pk == self.world.pk
            assert player_3.villages == 0
            assert player_3.points == 0
            assert player_3.tribe is not None
            assert player_3.tribe.tribe_id == 89
            player_4 = Player.objects.get(player_id=18244)
            assert player_4.name == "komar75"
            assert player_4.world.pk == self.world.pk
            assert player_4.villages == 1
            assert player_4.points == 2454
            assert player_4.tribe is not None
            assert player_4.tribe.tribe_id == 794
            player_5 = Player.objects.get(player_id=849015179)
            assert player_5.name == "szkutooMC"
            assert player_5.world.pk == self.world.pk
            assert player_5.villages == 1
            assert player_5.points == 200
            assert player_5.tribe is not None
            assert player_5.tribe.tribe_id == 381

            player_to_delete = Player.objects.filter(player_id=849015369)
            assert player_to_delete.exists()
            player_to_create = Player.objects.filter(player_id=849015399)
            assert not player_to_create.exists()

            village_1 = VillageModel.objects.get(village_id=1)
            assert village_1.player is not None
            assert village_1.player.player_id == 698870390
            assert village_1.world.pk == self.world.pk
            assert village_1.coord == "508|396"
            assert village_1.x_coord == 508
            assert village_1.y_coord == 396
            village_2 = VillageModel.objects.get(village_id=2)
            assert village_2.player is not None
            assert village_2.player.player_id == 2358891
            assert village_2.world.pk == self.world.pk
            assert village_2.coord == "546|483"
            assert village_2.x_coord == 546
            assert village_2.y_coord == 483
            village_41460 = VillageModel.objects.get(village_id=41460)
            assert village_41460.player is None
            assert village_41460.world.pk == self.world.pk
            assert village_41460.coord == "385|654"
            assert village_41460.x_coord == 385
            assert village_41460.y_coord == 654
            assert not VillageModel.objects.filter(village_id=41475).exists()

        with requests_mock.Mocker() as mock:
            world_query = WorldUpdateHandler(world=self.world)
            mock.get(
                world_query.world.link_to_game("/map/player.txt.gz"),
                content=PLAYERS_UPDATED,
                headers={
                    "etag": "123456",
                    "last-modified": "Mon, 09 May 2022 06:15:20 GMT",
                },
            )
            mock.get(
                world_query.world.link_to_game("/map/ally.txt.gz"),
                content=TRIBES_UPDATED,
                headers={
                    "etag": "123456",
                    "last-modified": "Mon, 09 May 2022 06:15:20 GMT",
                },
            )
            mock.get(
                world_query.world.link_to_game("/map/village.txt.gz"),
                content=VILLAGES_UPDATED,
                headers={
                    "etag": "123456",
                    "last-modified": "Mon, 09 May 2022 06:15:20 GMT",
                },
            )

            world_query.update_all()
            self.world.refresh_from_db()
            assert VillageModel.objects.count() == 38218
            assert Player.objects.count() == 10233
            assert Tribe.objects.count() == 534
            assert (
                self.world.fanout_key_text_player
                == "nt1_/map/player.txt.gz_1652076920.0"
            )
            assert (
                self.world.fanout_key_text_tribe == "nt1_/map/ally.txt.gz_1652076920.0"
            )
            assert (
                self.world.fanout_key_text_village
                == "nt1_/map/village.txt.gz_1652076920.0"
            )

            tribe_1 = Tribe.objects.get(tribe_id=30)
            assert tribe_1.world == self.world
            assert tribe_1.tag == "BNAp"
            tribe_2 = Tribe.objects.get(tribe_id=35)
            assert tribe_2.world == self.world
            assert tribe_2.tag == "BG"
            assert Tribe.objects.filter(tribe_id=2000).exists()
            assert not Tribe.objects.filter(tribe_id=1826).exists()

            player_1 = Player.objects.get(player_id=11480)
            assert player_1.name == "Nakon"
            assert player_1.world.pk == self.world.pk
            assert player_1.villages == 1
            assert player_1.points == 30
            assert player_1.tribe is not None
            assert player_1.tribe.tribe_id == 1097
            player_2 = Player.objects.get(player_id=39848)
            assert player_2.name == "polakumie"
            assert player_2.world.pk == self.world.pk
            assert player_2.villages == 21
            assert player_2.points == 257132
            assert player_2.tribe is not None
            assert player_2.tribe.tribe_id == 67
            player_3 = Player.objects.get(player_id=17714)
            assert player_3.name == "skobol235"
            assert player_3.world.pk == self.world.pk
            assert player_3.villages == 0
            assert player_3.points == 0
            assert player_3.tribe is not None
            assert player_3.tribe.tribe_id == 89
            player_4 = Player.objects.get(player_id=18244)
            assert player_4.name == "komar75"
            assert player_4.world.pk == self.world.pk
            assert player_4.villages == 1
            assert player_4.points == 3000
            assert player_4.tribe is not None
            assert player_4.tribe.tribe_id == 2000
            player_5 = Player.objects.get(player_id=849015179)
            assert player_5.name == "szkutooMC"
            assert player_5.world.pk == self.world.pk
            assert player_5.villages == 1
            assert player_5.points == 200
            assert player_5.tribe is not None
            assert player_5.tribe.tribe_id == 381

            player_to_delete = Player.objects.filter(player_id=849015369)
            assert not player_to_delete.exists()

            player_created = Player.objects.get(player_id=849015399)
            assert player_created.name == "rafsaf"
            assert player_created.world.pk == self.world.pk
            assert player_created.villages == 1
            assert player_created.points == 70
            assert player_created.tribe is None

            village_1 = VillageModel.objects.get(village_id=1)
            assert village_1.player is not None
            assert village_1.player.player_id == 849015399
            assert village_1.player.name == "rafsaf"
            assert village_1.world.pk == self.world.pk
            assert village_1.coord == "508|396"
            assert village_1.x_coord == 508
            assert village_1.y_coord == 396
            village_2 = VillageModel.objects.get(village_id=2)
            assert village_2.player is None
            assert village_2.world.pk == self.world.pk
            assert village_2.coord == "546|483"
            assert village_2.x_coord == 546
            assert village_2.y_coord == 483
            village_41460 = VillageModel.objects.get(village_id=41460)
            assert village_41460.player is not None
            assert village_41460.player.player_id == 6121024
            assert village_41460.world.pk == self.world.pk
            assert village_41460.coord == "385|654"
            assert village_41460.x_coord == 385
            assert village_41460.y_coord == 654
            village_41475 = VillageModel.objects.get(village_id=41475)
            assert village_41475.player is not None
            assert village_41475.player.player_id == 8728803
            assert village_41475.world.pk == self.world.pk
            assert village_41475.coord == "309|496"
            assert village_41475.x_coord == 309
            assert village_41475.y_coord == 496

    @freeze_time("2022-05-22 07:00:00")
    @patch("time.sleep", return_value=None)
    def test_db_update_cron_job_deletes_old_world_after_14d(
        self, patched_time_sleep
    ) -> None:
        self.world.save()
        with requests_mock.Mocker() as mock:
            world_query = WorldUpdateHandler(world=self.world)
            mock.get(
                world_query.world.link_to_game("/map/player.txt.gz"),
                content=PLAYERS,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            mock.get(
                world_query.world.link_to_game("/map/ally.txt.gz"),
                content=TRIBES,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            mock.get(
                world_query.world.link_to_game("/map/village.txt.gz"),
                content=VILLAGES,
                headers={
                    "etag": "12345",
                    "last-modified": "Sun, 08 May 2022 06:15:20 GMT",
                },
            )
            world_query.update_all()
            assert world_query.deleted
            assert World.objects.all().count() == 0
