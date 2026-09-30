# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from datetime import timedelta

from django.core.management import call_command

from base.models import Outline
from base.tests.test_utils.mini_setup import MiniSetup


class OutDateOutlineDelete(MiniSetup):
    def test_does_not_delete_now_outline(self):
        self.get_outline()
        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        call_command("outdateoutlinedelete")

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 1)

    def test_does_not_delete_outline_from_30_days(self):
        outline = self.get_outline()
        outline.created = outline.created - timedelta(days=30)
        outline.save()

        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        call_command("outdateoutlinedelete")

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 1)

    def test_does_not_delete_outline_from_34_days(self):
        outline = self.get_outline()
        outline.created = outline.created - timedelta(days=34)
        outline.save()

        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        call_command("outdateoutlinedelete")

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 1)

    def test_DOES_delete_outline_from_36_days(self):
        outline = self.get_outline()
        outline.created = outline.created - timedelta(days=36)
        outline.save()

        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        call_command("outdateoutlinedelete")

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 0)
