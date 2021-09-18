from pathlib import Path

import requests
import requests_mock

from base.cron import db_update
from base.models import Player, Tribe, VillageModel, World
from base.tests.test_utils.mini_setup import MiniSetup
from utils.database_update import WorldQuery

GET_CONFIG = Path("utils/tests/database_update/get_config.xml").read_text()
GET_UNIT_INFO = Path("utils/tests/database_update/get_unit_info.xml").read_text()


class WorldTest_check_if_world_exist_and_try_create(MiniSetup):
    def setUp(self):
        super().setUp()
        self.world = self.get_world(save=False)

    def test_already_added(self):
        world = self.world
        world.save()
        world_query = WorldQuery(world=world)
        assert world_query.check_if_world_exist_and_try_create() == (None, "added")

    def test_connection_error_get_config(self):
        world = self.world
        world_query = WorldQuery(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"),
                exc=requests.exceptions.RequestException,
            )
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_connection_bad_status_get_config(self):
        world = self.world
        world_query = WorldQuery(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"), status_code=400
            )
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_connection_redirect_get_config(self):
        world = self.world
        world_query = WorldQuery(world=world)
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
        world_query = WorldQuery(world=world)
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
                exc=requests.exceptions.RequestException,
            )
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_connection_bad_status_get_unit_info(self):
        world = self.world
        world_query = WorldQuery(world=world)
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
        world_query = WorldQuery(world=world)
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
        world_query = WorldQuery(world=world)
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
        world_query = WorldQuery(world=world)
        world_query.check_if_world_is_archived("https://example.com/archive/nt1")
        assert not World.objects.filter(pk=world.pk).exists()

    def test_if_world_if_archived2(self):
        world = self.world
        world.save()
        world.refresh_from_db()
        world_query = WorldQuery(world=world)
        world_query.check_if_world_is_archived("https://example.com/archive/nope")
        assert World.objects.filter(pk=world.pk).exists()
        assert world_query.world.connection_errors == 1

    def test_db_update_cron_job(self):
        TRIBES = Path("utils/tests/database_update/ally.txt").read_text()
        PLAYERS = Path("utils/tests/database_update/player.txt").read_text()
        VILLAGES = Path("utils/tests/database_update/village.txt").read_text()
        self.world.save()
        world_query = WorldQuery(world=self.world)
        with requests_mock.Mocker() as mock:
            mock.get(world_query.world.link_to_game("/map/player.txt"), text=PLAYERS)
            mock.get(world_query.world.link_to_game("/map/ally.txt"), text=TRIBES)
            mock.get(world_query.world.link_to_game("/map/village.txt"), text=VILLAGES)
            db_update()
            self.world.refresh_from_db()
            date1 = self.world.last_update
            assert VillageModel.objects.count() == 38219
            assert Player.objects.count() == 10234
            assert Tribe.objects.count() == 534
            db_update()
            self.world.refresh_from_db()
            date2 = self.world.last_update
            assert date2 > date1
