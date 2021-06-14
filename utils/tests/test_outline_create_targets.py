from typing import List

from django.test import TestCase
from django.utils.translation import activate

from base.models import Outline
from base.models import TargetVertex as Target
from base.tests.test_utils.initial_setup import create_initial_data_write_outline
from utils.basic import TargetMode
from utils.outline_create_targets import OutlineCreateTargets


class TestOutlineCreateTargets(TestCase):
    def setUp(self):
        activate("pl")
        create_initial_data_write_outline()
        self.outline: Outline = Outline.objects.get(id=1)

    def test_creates_real_targets_properly_standard_syntax(self):
        target_mode = TargetMode("real")
        input: str = "500|499:2:5"
        self.outline.initial_outline_targets = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        target: Target = Target.objects.get(target="500|499", outline=self.outline)
        self.assertEqual(target.fake, False)
        self.assertEqual(target.ruin, False)
        self.assertEqual(target.required_off, 2)
        self.assertEqual(target.required_noble, 5)
        self.assertEqual(target.exact_off, [])
        self.assertEqual(target.exact_noble, [])

    def test_creates_fake_targets_properly_standard_syntax(self):
        target_mode = TargetMode("fake")
        input: str = "500|499:2:5"
        self.outline.initial_outline_fakes = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        target: Target = Target.objects.get(target="500|499", outline=self.outline)
        self.assertEqual(target.fake, True)
        self.assertEqual(target.ruin, False)
        self.assertEqual(target.required_off, 2)
        self.assertEqual(target.required_noble, 5)
        self.assertEqual(target.exact_off, [])
        self.assertEqual(target.exact_noble, [])

    def test_creates_ruin_targets_properly_standard_syntax(self):
        target_mode = TargetMode("ruin")
        input: str = "500|499:2:5"
        self.outline.initial_outline_ruins = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        target: Target = Target.objects.get(target="500|499", outline=self.outline)
        self.assertEqual(target.fake, False)
        self.assertEqual(target.ruin, True)
        self.assertEqual(target.required_off, 2)
        self.assertEqual(target.required_noble, 5)
        self.assertEqual(target.exact_off, [])
        self.assertEqual(target.exact_noble, [])

    def test_creates_real_targets_properly_extended_syntax(self):
        target_mode = TargetMode("real")
        input: str = "500|499:2|1|1|2:5|4|4|4"
        self.outline.initial_outline_targets = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        target: Target = Target.objects.get(target="500|499", outline=self.outline)
        self.assertEqual(target.fake, False)
        self.assertEqual(target.ruin, False)
        self.assertEqual(target.required_off, 0)
        self.assertEqual(target.required_noble, 0)
        self.assertEqual(target.exact_off, [2, 1, 1, 2])
        self.assertEqual(target.exact_noble, [5, 4, 4, 4])

    def test_creates_fake_targets_properly_extended_syntax(self):
        target_mode = TargetMode("fake")
        input: str = "500|499:2|1|1|2:5|4|4|4"
        self.outline.initial_outline_fakes = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        target: Target = Target.objects.get(target="500|499", outline=self.outline)
        self.assertEqual(target.fake, True)
        self.assertEqual(target.ruin, False)
        self.assertEqual(target.required_off, 0)
        self.assertEqual(target.required_noble, 0)
        self.assertEqual(target.exact_off, [2, 1, 1, 2])
        self.assertEqual(target.exact_noble, [5, 4, 4, 4])

    def test_creates_ruin_targets_properly_extended_syntax(self):
        target_mode = TargetMode("ruin")
        input: str = "500|499:2|1|1|2:5|4|4|4"
        self.outline.initial_outline_ruins = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        target: Target = Target.objects.get(target="500|499", outline=self.outline)
        self.assertEqual(target.fake, False)
        self.assertEqual(target.ruin, True)
        self.assertEqual(target.required_off, 0)
        self.assertEqual(target.required_noble, 0)
        self.assertEqual(target.exact_off, [2, 1, 1, 2])
        self.assertEqual(target.exact_noble, [5, 4, 4, 4])

    def test_real_targets_properly_creates_many_diffrent_syntax_targets(self):
        target_mode = TargetMode("real")
        input: str = "500|499:1:1\r\n500|499:1|1|1|1:4\r\n500|499:4:2|2|2|2\r\n500|499:0|0|0|0:0|0|0|0"
        self.outline.initial_outline_targets = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        targets: List[Target] = list(
            Target.objects.filter(outline=self.outline).order_by("pk")
        )

        self.assertEqual(targets[0].fake, False)
        self.assertEqual(targets[0].ruin, False)
        self.assertEqual(targets[0].required_off, 1)
        self.assertEqual(targets[0].required_noble, 1)
        self.assertEqual(targets[0].exact_off, [])
        self.assertEqual(targets[0].exact_noble, [])

        self.assertEqual(targets[1].fake, False)
        self.assertEqual(targets[1].ruin, False)
        self.assertEqual(targets[1].required_off, 0)
        self.assertEqual(targets[1].required_noble, 4)
        self.assertEqual(targets[1].exact_off, [1, 1, 1, 1])
        self.assertEqual(targets[1].exact_noble, [])

        self.assertEqual(targets[2].fake, False)
        self.assertEqual(targets[2].ruin, False)
        self.assertEqual(targets[2].required_off, 4)
        self.assertEqual(targets[2].required_noble, 0)
        self.assertEqual(targets[2].exact_off, [])
        self.assertEqual(targets[2].exact_noble, [2, 2, 2, 2])

        self.assertEqual(targets[3].fake, False)
        self.assertEqual(targets[3].ruin, False)
        self.assertEqual(targets[3].required_off, 0)
        self.assertEqual(targets[3].required_noble, 0)
        self.assertEqual(targets[3].exact_off, [0, 0, 0, 0])
        self.assertEqual(targets[3].exact_noble, [0, 0, 0, 0])

    def test_ruin_targets_properly_creates_many_diffrent_syntax_targets(self):
        target_mode = TargetMode("ruin")
        input: str = "500|499:1:1\r\n500|499:1|1|1|1:4\r\n500|499:4:2|2|2|2\r\n500|499:0|0|0|0:0|0|0|0"
        self.outline.initial_outline_ruins = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        targets: List[Target] = list(
            Target.objects.filter(outline=self.outline).order_by("pk")
        )

        self.assertEqual(targets[0].fake, False)
        self.assertEqual(targets[0].ruin, True)
        self.assertEqual(targets[0].required_off, 1)
        self.assertEqual(targets[0].required_noble, 1)
        self.assertEqual(targets[0].exact_off, [])
        self.assertEqual(targets[0].exact_noble, [])

        self.assertEqual(targets[1].fake, False)
        self.assertEqual(targets[1].ruin, True)
        self.assertEqual(targets[1].required_off, 0)
        self.assertEqual(targets[1].required_noble, 4)
        self.assertEqual(targets[1].exact_off, [1, 1, 1, 1])
        self.assertEqual(targets[1].exact_noble, [])

        self.assertEqual(targets[2].fake, False)
        self.assertEqual(targets[2].ruin, True)
        self.assertEqual(targets[2].required_off, 4)
        self.assertEqual(targets[2].required_noble, 0)
        self.assertEqual(targets[2].exact_off, [])
        self.assertEqual(targets[2].exact_noble, [2, 2, 2, 2])

        self.assertEqual(targets[3].fake, False)
        self.assertEqual(targets[3].ruin, True)
        self.assertEqual(targets[3].required_off, 0)
        self.assertEqual(targets[3].required_noble, 0)
        self.assertEqual(targets[3].exact_off, [0, 0, 0, 0])
        self.assertEqual(targets[3].exact_noble, [0, 0, 0, 0])

    def test_fake_targets_properly_creates_many_diffrent_syntax_targets(self):
        target_mode = TargetMode("fake")
        input: str = "500|499:1:1\r\n500|499:1|1|1|1:4\r\n500|499:4:2|2|2|2\r\n500|499:0|0|0|0:0|0|0|0"
        self.outline.initial_outline_fakes = input
        create_targets = OutlineCreateTargets(self.outline, target_mode)
        create_targets()
        targets: List[Target] = list(
            Target.objects.filter(outline=self.outline).order_by("pk")
        )

        self.assertEqual(targets[0].fake, True)
        self.assertEqual(targets[0].ruin, False)
        self.assertEqual(targets[0].required_off, 1)
        self.assertEqual(targets[0].required_noble, 1)
        self.assertEqual(targets[0].exact_off, [])
        self.assertEqual(targets[0].exact_noble, [])

        self.assertEqual(targets[1].fake, True)
        self.assertEqual(targets[1].ruin, False)
        self.assertEqual(targets[1].required_off, 0)
        self.assertEqual(targets[1].required_noble, 4)
        self.assertEqual(targets[1].exact_off, [1, 1, 1, 1])
        self.assertEqual(targets[1].exact_noble, [])

        self.assertEqual(targets[2].fake, True)
        self.assertEqual(targets[2].ruin, False)
        self.assertEqual(targets[2].required_off, 4)
        self.assertEqual(targets[2].required_noble, 0)
        self.assertEqual(targets[2].exact_off, [])
        self.assertEqual(targets[2].exact_noble, [2, 2, 2, 2])

        self.assertEqual(targets[3].fake, True)
        self.assertEqual(targets[3].ruin, False)
        self.assertEqual(targets[3].required_off, 0)
        self.assertEqual(targets[3].required_noble, 0)
        self.assertEqual(targets[3].exact_off, [0, 0, 0, 0])
        self.assertEqual(targets[3].exact_noble, [0, 0, 0, 0])
