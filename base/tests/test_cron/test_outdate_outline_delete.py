from datetime import timedelta

from base.cron import outdate_outline_delete
from base.models import Outline
from base.tests.test_utils.mini_setup import MiniSetup


class OutDateOutlineDelete(MiniSetup):
    def test_does_not_delete_now_outline(self):
        self.get_outline()
        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        outdate_outline_delete()

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 1)

    def test_does_not_delete_outline_from_30_days(self):
        outline = self.get_outline()
        outline.created = outline.created - timedelta(days=30)
        outline.save()

        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        outdate_outline_delete()

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 1)

    def test_does_not_delete_outline_from_34_days(self):
        outline = self.get_outline()
        outline.created = outline.created - timedelta(days=34)
        outline.save()

        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        outdate_outline_delete()

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 1)

    def test_DOES_delete_outline_from_36_days(self):
        outline = self.get_outline()
        outline.created = outline.created - timedelta(days=36)
        outline.save()

        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        outdate_outline_delete()

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 0)

    def test_DOES_NOT_delete_outline_from_36_days_if_test_world(self):
        outline = self.get_outline(test_world=True)
        outline.created = outline.created - timedelta(days=36)
        outline.save()

        count1: int = Outline.objects.count()
        self.assertEqual(count1, 1)

        outdate_outline_delete()

        count2: int = Outline.objects.count()
        self.assertEqual(count2, 1)
