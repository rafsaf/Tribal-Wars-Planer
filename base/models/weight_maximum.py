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

from copy import deepcopy
from typing import TYPE_CHECKING

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class WeightMaximum(models.Model):
    """Control state smaller than maximum"""

    outline = models.ForeignKey("Outline", on_delete=models.CASCADE, db_index=True)
    start = models.CharField(max_length=7, db_index=True)
    x_coord = models.IntegerField(default=0)
    y_coord = models.IntegerField(default=0)
    player = models.CharField(max_length=30)

    off_max = models.IntegerField()
    off_state = models.IntegerField(default=0)
    off_left = models.IntegerField()

    nobleman_max = models.IntegerField()
    nobleman_state = models.IntegerField(default=0)
    nobleman_left = models.IntegerField()

    catapult_max = models.IntegerField(default=0)
    catapult_state = models.IntegerField(default=0)
    catapult_left = models.IntegerField(default=0)

    hidden = models.BooleanField(default=False)
    first_line = models.BooleanField(default=False)
    too_far_away = models.BooleanField(default=False)
    fake_limit = models.IntegerField(
        default=4, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    if TYPE_CHECKING:
        distance: int
        night_bool: bool

    CHANGES_TRACKED_FIELDS = [
        "off_left",
        "off_state",
        "nobleman_left",
        "nobleman_state",
        "catapult_left",
        "catapult_state",
        "fake_limit",
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.CHANGES_TRACKED_FIELDS:
            setattr(self, f"_original_{field}", deepcopy(getattr(self, field)))

    def __str__(self):
        return self.start

    def coord_tuple(self):
        return (self.x_coord, self.y_coord)

    @property
    def has_changed(self):
        for field in self.CHANGES_TRACKED_FIELDS:
            if getattr(self, f"_original_{field}") != getattr(self, field):
                return True
        return False
