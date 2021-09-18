from base.tests.test_utils.mini_setup import MiniSetup


class WorldTest(MiniSetup):
    def test__str__(self):
        world = self.get_world()
        assert str(world) == "nt1"

    def test_human_prefix_true(self):
        world = self.get_world()
        assert world.human(prefix=True) == "Świat 1 NT"

    def test_human_prefix_false(self):
        world = self.get_world()
        assert world.human(prefix=False) == "Świat 1"

    def test_link_to_game(self):
        world = self.get_world()
        link = world.link_to_game(addition="+my addition")

        assert link == "https://nt1.nottestserver+my addition"

    def test_tw_stats_link_to_village(self):
        world = self.get_world()
        link = world.tw_stats_link_to_village("1000")

        assert link == ("https://nt.twstats.com/nt1/index.php?" "page=village&id=1000")
