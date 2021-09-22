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
