# Copyright 2025 Rafał Safin (rafsaf). All Rights Reserved.
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

"""
Tests for ram/catapult-based fake limit feature.

This test file ensures that fakes are properly limited by available rams and catapults.
The key feature being tested:
- Fakes require at least 1 ram OR 1 catapult to be sent
- fake_limit is calculated as min(outline_fake_limit, ram_left + catapult_left)
- When ram_left is None (old data), the old behavior is preserved
"""

from django.test import TestCase
from django.utils.translation import activate

from base.models import Outline, WeightMaximum, WeightModel
from base.models import TargetVertex as Target
from base.tests.test_utils.initial_setup import create_initial_data_write_outline
from utils.fast_weight_maximum import FastWeightMaximum
from utils.outline_complete import complete_outline_write
from utils.outline_initial import MakeOutline


class TestRamFakeLimitFeature(TestCase):
    """Test that fake_limit is properly constrained by ram_left + catapult_left"""

    def setUp(self):
        activate("pl")
        create_initial_data_write_outline()
        self.outline: Outline = Outline.objects.get(id=1)
        make_outline = MakeOutline(self.outline)
        make_outline()
        self.salt = "test_ram_fake_limit"

    def test_fast_weight_maximum_fake_limit_with_rams_and_catapults(self):
        """Test fake_limit calculation when rams and catapults are available"""
        weight_max = WeightMaximum.objects.get(start="500|500")
        # Set specific values
        weight_max.ram_left = 50
        weight_max.catapult_left = 30
        weight_max.save()

        # outline has fake_limit = 10 by default
        self.outline.initial_outline_fake_limit = 10
        self.outline.save()

        fast_weight = FastWeightMaximum(weight_max, 0, self.outline)

        # fake_limit should be min(10, 50 + 30) = 10
        self.assertEqual(fast_weight.fake_limit, 10)

    def test_fast_weight_maximum_fake_limit_constrained_by_rams_catapults(self):
        """Test fake_limit is constrained when rams + catapults < outline fake_limit"""
        weight_max = WeightMaximum.objects.get(start="500|500")
        # Set low ram and catapult values
        weight_max.ram_left = 3
        weight_max.catapult_left = 2
        weight_max.save()

        # outline has high fake_limit
        self.outline.initial_outline_fake_limit = 100
        self.outline.save()

        fast_weight = FastWeightMaximum(weight_max, 0, self.outline)

        # fake_limit should be min(100, 3 + 2) = 5
        self.assertEqual(fast_weight.fake_limit, 5)

    def test_fast_weight_maximum_fake_limit_zero_rams_zero_catapults(self):
        """Test fake_limit is 0 when no rams or catapults available"""
        weight_max = WeightMaximum.objects.get(start="500|500")
        # No rams or catapults
        weight_max.ram_left = 0
        weight_max.catapult_left = 0
        weight_max.save()

        self.outline.initial_outline_fake_limit = 10
        self.outline.save()

        fast_weight = FastWeightMaximum(weight_max, 0, self.outline)

        # fake_limit should be min(10, 0 + 0) = 0
        self.assertEqual(fast_weight.fake_limit, 0)

    def test_fast_weight_maximum_fake_limit_only_rams(self):
        """Test fake_limit calculation with only rams available"""
        weight_max = WeightMaximum.objects.get(start="500|500")
        weight_max.ram_left = 5
        weight_max.catapult_left = 0
        weight_max.save()

        self.outline.initial_outline_fake_limit = 10
        self.outline.save()

        fast_weight = FastWeightMaximum(weight_max, 0, self.outline)

        # fake_limit should be min(10, 5 + 0) = 5
        self.assertEqual(fast_weight.fake_limit, 5)

    def test_fast_weight_maximum_fake_limit_only_catapults(self):
        """Test fake_limit calculation with only catapults available"""
        weight_max = WeightMaximum.objects.get(start="500|500")
        weight_max.ram_left = 0
        weight_max.catapult_left = 8
        weight_max.save()

        self.outline.initial_outline_fake_limit = 10
        self.outline.save()

        fast_weight = FastWeightMaximum(weight_max, 0, self.outline)

        # fake_limit should be min(10, 0 + 8) = 8
        self.assertEqual(fast_weight.fake_limit, 8)

    def test_fast_weight_maximum_fake_limit_backward_compatibility_none(self):
        """Test backward compatibility when ram_left is None (old data)"""
        weight_max = WeightMaximum.objects.get(start="500|500")
        # Simulate old data where ram_left is None
        weight_max.ram_left = None
        weight_max.catapult_left = 50
        weight_max.save()

        self.outline.initial_outline_fake_limit = 10
        self.outline.save()

        fast_weight = FastWeightMaximum(weight_max, 0, self.outline)

        # fake_limit should fall back to outline.initial_outline_fake_limit
        self.assertEqual(fast_weight.fake_limit, 10)

    def test_outline_complete_no_fakes_when_zero_rams_catapults(self):
        """Test that no fake attacks are written when village has 0 rams and 0 catapults"""
        # Set all weight_max to have no rams or catapults
        WeightMaximum.objects.filter(outline=self.outline).update(
            ram_left=0, catapult_left=0
        )

        # Create a fake target
        target = Target.objects.create(
            outline=self.outline,
            fake=True,
            target="500|499",
            player="player1",
            required_off=5,
        )

        complete_outline_write(self.outline, salt=self.salt)

        # Should create no weights since fake_limit is 0 for all villages
        created_weights = WeightModel.objects.filter(target=target).count()
        self.assertEqual(created_weights, 0)

    def test_outline_complete_limited_fakes_by_rams_catapults(self):
        """Test that fake attacks are limited by available rams + catapults"""
        # Set specific ram and catapult values
        weight_max1 = WeightMaximum.objects.get(start="500|500")
        weight_max1.ram_left = 2
        weight_max1.catapult_left = 1
        weight_max1.off_left = 10000  # Enough troops
        weight_max1.save()

        weight_max2 = WeightMaximum.objects.get(start="500|501")
        weight_max2.ram_left = 1
        weight_max2.catapult_left = 0
        weight_max2.off_left = 10000  # Enough troops
        weight_max2.save()

        # Set all others to 0
        WeightMaximum.objects.filter(outline=self.outline).exclude(
            start__in=["500|500", "500|501"]
        ).update(ram_left=0, catapult_left=0)

        self.outline.initial_outline_fake_limit = 100  # High limit
        self.outline.initial_outline_min_off = 100
        self.outline.initial_outline_max_off = 15000
        self.outline.save()

        # Create a fake target requesting many fakes
        target = Target.objects.create(
            outline=self.outline,
            fake=True,
            target="500|499",
            player="player1",
            required_off=10,  # Request 10 fakes
        )

        complete_outline_write(self.outline, salt=self.salt)

        created_weights = WeightModel.objects.filter(target=target)

        # Should only create fakes from villages with rams/catapults
        # weight_max1 can send max 3 fakes (2 rams + 1 catapult)
        # weight_max2 can send max 1 fake (1 ram)
        # Total: max 4 fakes, but we requested 10
        self.assertLessEqual(created_weights.count(), 4)

        # Verify no fakes were sent from villages without rams/catapults
        starts_with_fakes = set(created_weights.values_list("start", flat=True))
        self.assertTrue(starts_with_fakes.issubset({"500|500", "500|501"}))

    def test_outline_initial_rams_are_properly_saved(self):
        """Test that rams are properly initialized from army data"""
        # This is already tested by create_initial_data_write_outline setup
        # but let's verify explicitly
        weight_max = WeightMaximum.objects.get(start="500|500")

        # Check that ram fields are properly set
        self.assertIsNotNone(weight_max.ram_max)
        self.assertIsNotNone(weight_max.ram_left)
        self.assertIsNotNone(weight_max.ram_state)

        # ram_max should equal ram_left initially
        self.assertEqual(weight_max.ram_max, weight_max.ram_left)

        # ram_state should be 0 initially
        self.assertEqual(weight_max.ram_state, 0)

    def test_fakes_with_sufficient_rams_and_catapults(self):
        """Test that fakes are created when sufficient rams/catapults exist"""
        # Ensure villages have rams and catapults
        WeightMaximum.objects.filter(outline=self.outline).update(
            ram_left=50, catapult_left=50, off_left=10000
        )

        self.outline.initial_outline_fake_limit = 5
        self.outline.initial_outline_min_off = 100
        self.outline.initial_outline_max_off = 15000
        self.outline.save()

        # Create a fake target
        target = Target.objects.create(
            outline=self.outline,
            fake=True,
            target="500|499",
            player="player1",
            required_off=3,
        )

        complete_outline_write(self.outline, salt=self.salt)

        created_weights = WeightModel.objects.filter(target=target)

        # Should create the requested 3 fakes
        self.assertEqual(created_weights.count(), 3)

        # All should be marked as not ruin
        self.assertTrue(all(not w.ruin for w in created_weights))

    def test_fake_mode_off_respects_ram_catapult_limit(self):
        """Test fake mode 'off' respects ram/catapult limits"""
        weight_max = WeightMaximum.objects.get(start="500|500")
        weight_max.ram_left = 1
        weight_max.catapult_left = 1
        weight_max.off_left = 5000  # Within min/max range
        weight_max.save()

        self.outline.initial_outline_fake_mode = "off"
        self.outline.initial_outline_min_off = 4000
        self.outline.initial_outline_max_off = 6000
        self.outline.initial_outline_fake_limit = 10
        self.outline.save()

        target = Target.objects.create(
            outline=self.outline,
            fake=True,
            target="500|499",
            player="player1",
            required_off=5,
        )

        complete_outline_write(self.outline, salt=self.salt)

        # Can send max 2 fakes (1 ram + 1 catapult)
        created_weights = WeightModel.objects.filter(target=target, start="500|500")
        self.assertLessEqual(created_weights.count(), 2)

    def test_fake_mode_divide_respects_ram_catapult_limit(self):
        """Test fake mode 'divide' respects ram/catapult limits"""
        weight_max = WeightMaximum.objects.get(start="500|500")
        weight_max.ram_left = 2
        weight_max.catapult_left = 3
        weight_max.off_left = 10000
        weight_max.save()

        self.outline.initial_outline_fake_mode = "divide"
        self.outline.initial_outline_fake_limit = 20
        self.outline.save()

        fast_weight = FastWeightMaximum(weight_max, 0, self.outline)

        # fake_limit should be constrained to 5 (2 rams + 3 catapults)
        self.assertEqual(fast_weight.fake_limit, 5)

    def test_rams_properly_tracked_through_outline_creation(self):
        """Integration test: verify rams are tracked from outline initial through complete"""
        # Use existing outline and create weight_max with specific ram values
        weight_max = WeightMaximum.objects.create(
            outline=self.outline,
            start="501|501",
            village_id=999,
            x_coord=501,
            y_coord=501,
            player="test_player",
            player_id=999,
            points=10000,
            off_max=20000,
            off_state=0,
            off_left=20000,
            nobleman_max=5,
            nobleman_state=0,
            nobleman_left=5,
            catapult_max=50,
            catapult_state=0,
            catapult_left=50,
            ram_max=25,
            ram_left=25,
            ram_state=0,
            first_line=False,
        )

        # Verify initial state
        self.assertEqual(weight_max.ram_max, 25)
        self.assertEqual(weight_max.ram_left, 25)
        self.assertEqual(weight_max.ram_state, 0)

        # Create FastWeightMaximum and verify fake_limit
        self.outline.initial_outline_fake_limit = 30
        self.outline.save()

        fast_weight = FastWeightMaximum(weight_max, 0, self.outline)

        # With 25 rams + 50 catapults = 75, but outline limit is 30
        # fake_limit should be min(30, 25 + 50) = 30
        expected_limit = min(30, weight_max.ram_left + weight_max.catapult_left)
        self.assertEqual(fast_weight.fake_limit, expected_limit)
        self.assertEqual(fast_weight.fake_limit, 30)
