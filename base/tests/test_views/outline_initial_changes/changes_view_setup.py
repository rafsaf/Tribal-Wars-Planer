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

import random
import string

from django.test import TestCase

from base.models import Outline, TargetVertex, WeightMaximum, WeightModel
from base.tests.test_utils.initial_setup import create_initial_data


class ChangesViewSetup(TestCase):
    def setUp(self):
        create_initial_data()

    def get_outline(self) -> Outline:
        return Outline.objects.get(pk=1)

    def get_target(self, outline: Outline, coord: str = "500|499") -> TargetVertex:
        return TargetVertex.objects.get(target=coord, outline=outline)

    def get_weight_max(self, outline: Outline, start: str = "500|500") -> WeightMaximum:
        return WeightMaximum.objects.get(outline=outline, start=start)

    def get_weight(self, target: TargetVertex, start: str = "500|500") -> WeightModel:
        return WeightModel.objects.get(target=target, start=start)

    def random_lower_string(self, length=20) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=length))
