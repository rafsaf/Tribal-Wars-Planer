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

import requests
import requests_mock

from base.models import Player, Tribe, VillageModel, World
from base.tests.test_utils.mini_setup import MiniSetup
from utils.database_update import WorldUpdateHandler

CURRENT_DIRECTORY = Path(__file__).parent
GET_CONFIG = (CURRENT_DIRECTORY / "database_update/get_config.xml").read_text()
GET_UNIT_INFO = (CURRENT_DIRECTORY / "database_update/get_unit_info.xml").read_text()
TRIBES = (CURRENT_DIRECTORY / "database_update/ally.txt.gz").read_bytes()
PLAYERS = (CURRENT_DIRECTORY / "database_update/player.txt.gz").read_bytes()
VILLAGES = (CURRENT_DIRECTORY / "database_update/village.txt.gz").read_bytes()


class WorldUpdateHandlerTest(MiniSetup):
    def setUp(self):
        super().setUp()
        self.world = self.get_world(save=False)

    def test_already_added(self):
        world = self.world
        world.save()
        world_query = WorldUpdateHandler(world=world)
        assert world_query.check_if_world_exist_and_try_create() == (None, "added")

    def test_connection_error_get_config(self):
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"),
                exc=requests.exceptions.ConnectionError,
            )
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_connection_bad_status_get_config(self):
        world = self.world
        world_query = WorldUpdateHandler(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"), status_code=400
            )
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_connection_redirect_get_config(self):
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
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_connection_error_get_unit_info(self):
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
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_connection_bad_status_get_unit_info(self):
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
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_connection_redirect_get_unit_info(self):
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
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_works_ok(self):
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
            assert world_query.check_if_world_exist_and_try_create() == (
                world_query.world,
                "success",
            )
        world_query.world.refresh_from_db()
        assert world_query.world.speed_world == 1.6
        assert world_query.world.speed_units == 0.625
        assert world_query.world.paladin == "active"
        assert world_query.world.archer == "active"
        assert world_query.world.militia == "active"

    def test_if_world_if_archived1(self):
        world = self.world
        world.save()
        world.refresh_from_db()
        world_query = WorldUpdateHandler(world=world)
        world_query.check_if_world_is_archived("https://example.com/archive/nt1")
        assert not World.objects.filter(pk=world.pk).exists()

    def test_if_world_if_archived2(self):
        world = self.world
        world.save()
        world.refresh_from_db()
        world_query = WorldUpdateHandler(world=world)
        world_query.check_if_world_is_archived("https://example.com/archive/nope")
        assert World.objects.filter(pk=world.pk).exists()
        assert world_query.world.connection_errors == 1

    def test_last_modified_timestamp(self):
        datetime = "Sat, 08 Jan 2022 13:48:44 GMT"
        assert WorldUpdateHandler.last_modified_timestamp(datetime) == 1641649724

    @patch("time.sleep", return_value=None)
    def test_db_update_cron_job(self, patched_time_sleep):
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
            world_query.update_all()
            self.world.refresh_from_db()
            date2 = self.world.updated_at
            assert date2 > date1
