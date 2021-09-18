from pathlib import Path

import requests_mock

from base.tests.test_utils.mini_setup import MiniSetup
from utils.database_update import WorldQuery

GET_CONFIG = Path("utils/tests/database_update/get_config.xml").read_text()
GET_UNIT_INFO = Path("utils/tests/database_update/get_config.xml").read_text()


class WorldTest(MiniSetup):
    def setUp(self):
        super().setUp()
        self.world = self.get_world(save=False)

    def test_check_if_world_exist_and_try_create_created_return_none(self):
        world = self.world
        world.save()
        world_query = WorldQuery(world=world)
        assert world_query.check_if_world_exist_and_try_create() == (None, "added")
        # requests_mock.get(world.link_to_game("/interface.php?func=get_config"), status_code=200)

    def test_check_if_world_exist_and_try_create_create(self):
        world = self.world
        world_query = WorldQuery(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                world.link_to_game("/interface.php?func=get_config"), status_code=404
            )
            assert world_query.check_if_world_exist_and_try_create() == (None, "error")

    def test_check_if_world_exist_and_try_create_create_works_ok(self):
        world = self.world
        world_query = WorldQuery(world=world)
        with requests_mock.Mocker() as mock:
            mock.get(
                self.world.link_to_game("/interface.php?func=get_config"),
                text=GET_CONFIG,
                status_code=200,
            )
            mock.get(
                self.world.link_to_game("/interface.php?func=get_unit_info"),
                text=GET_UNIT_INFO,
                status_code=200,
            )
            assert world_query.check_if_world_exist_and_try_create() == (
                world,
                "success",
            )
        world.refresh_from_db()
        assert world.speed_world == 1.6
        assert world.speed_units == 0.625
