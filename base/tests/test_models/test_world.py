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
