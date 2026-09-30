# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.utils.translation import activate

from base.tests.test_utils.mini_setup import MiniSetup


class WorldTest(MiniSetup):
    def test_human_prefix_true(self):
        activate("pl")
        world = self.get_world()
        assert world.human(prefix=True) == "Świat 1 NT"

    def test_human_prefix_false(self):
        activate("pl")
        world = self.get_world()
        assert world.human(prefix=False) == "Świat 1"

    def test_game_name_prefix_true(self):
        activate("pl")
        world = self.get_world()
        world.full_game_name = "Świat 1"
        assert world.human(prefix=True) == "Świat 1 NT"

    def test_game_name_prefix_false(self):
        activate("pl")
        world = self.get_world()
        world.full_game_name = "Świat 1"
        assert world.human(prefix=False) == "Świat 1"

    def test_link_to_game(self):
        world = self.get_world()
        link = world.link_to_game(addition="+my addition")

        assert link == "https://nt1.nottestserver+my addition"

    def test_tw_stats_link_to_village(self):
        world = self.get_world()
        link = world.tw_stats_link_to_village("1000")

        assert link == "https://nt.twstats.com/nt1/index.php?page=village&id=1000"
