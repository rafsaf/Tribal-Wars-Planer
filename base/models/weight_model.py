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

from collections.abc import Callable
from datetime import datetime
from math import sqrt

from django.db import models

from base.models.target_vertex import TargetVertex
from base.models.weight_maximum import WeightMaximum
from utils.buildings import BUILDINGS_TRANSLATION


class WeightModel(models.Model):
    """Command between start and target"""

    BUILDINGS = BUILDINGS_TRANSLATION.items()

    target = models.ForeignKey(TargetVertex, on_delete=models.CASCADE, db_index=True)
    state = models.ForeignKey(WeightMaximum, on_delete=models.CASCADE)
    start = models.CharField(max_length=7)
    village_id = models.IntegerField()
    off = models.IntegerField()
    distance = models.FloatField()
    nobleman = models.IntegerField()
    catapult = models.IntegerField()
    ruin = models.BooleanField()
    building = models.CharField(max_length=50, choices=BUILDINGS, null=True, blank=True)
    order = models.IntegerField()
    player = models.CharField(max_length=40)
    player_id = models.IntegerField()
    first_line = models.BooleanField()

    t1: datetime
    t2: datetime
    sh_t1: datetime
    sh_t2: datetime
    get_building_display: Callable[[], str]

    def __str__(self):
        return self.start

    def distance_to_village(self, coord: str) -> float:
        return sqrt(
            (int(self.start[0:3]) - int(coord[0:3])) ** 2
            + (int(self.start[4:7]) - int(coord[4:7])) ** 2
        )
