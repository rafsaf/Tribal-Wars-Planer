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

from typing import TYPE_CHECKING, Self

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from base.models.outline import Outline


class WeightMaximum(models.Model):
    """Control state smaller than maximum"""

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE, db_index=True)
    start = models.CharField(max_length=7)
    x_coord = models.IntegerField(default=0)
    y_coord = models.IntegerField(default=0)
    player = models.CharField(max_length=30)
    points = models.IntegerField(default=0)

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
    nobles_limit = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(250)],
    )

    if TYPE_CHECKING:
        distance: float
        night_bool: bool
        morale: int

    CHANGES_TRACKED_FIELDS = [
        "off_left",
        "off_state",
        "nobleman_left",
        "nobleman_state",
        "catapult_left",
        "catapult_state",
        "fake_limit",
        "nobles_limit",
    ]

    def __str__(self):
        return self.start

    def coord_tuple(self):
        return (self.x_coord, self.y_coord)

    @property
    def nobles_allowed_to_use(self) -> int:
        if self.outline.initial_outline_minimum_noble_troops == 0:
            possible_nobles_by_min_off = self.nobleman_left
        else:
            possible_nobles_by_min_off = (
                self.off_left // self.outline.initial_outline_minimum_noble_troops
            )
        return min(self.nobleman_left, self.nobles_limit, possible_nobles_by_min_off)

    @property
    def has_changed(self):
        for field in self.CHANGES_TRACKED_FIELDS:
            if getattr(self, f"_original_{field}") != getattr(self, field):
                return True
        return False


class FastWeightMaximum:
    """
    Why this class exists?

    This class is used to speed up the process of calculating the outline.
    It is used in the outline_complete.py file, where the outline is calculated.

    The outline calculation is a very time-consuming process.
    Worst part was related to access to getable fields in the WeightMaximum model.
    It's very magic how field __get__ and __set__ methods are resolved in Django ORM,
    and it's really slow. It's completely not designed for such a high number of accesses.
    """

    def __init__(self, weight_max: WeightMaximum, index: int, outline: Outline) -> None:
        # index is a list index in the outline list of real WeightMaximum objects
        # so they can be updated in the same place after calculations
        self.index: int = index

        self.pk = weight_max.pk
        self.start: str = weight_max.start
        self.coord_tuple: tuple[int, int] = (weight_max.x_coord, weight_max.y_coord)
        self.player: str = weight_max.player
        self.points: int = weight_max.points
        self.off_state: int = weight_max.off_state
        self.off_left: int = weight_max.off_left
        self.nobleman_state: int = weight_max.nobleman_state
        self.nobleman_left: int = weight_max.nobleman_left
        self.catapult_state: int = weight_max.catapult_state
        self.catapult_left: int = weight_max.catapult_left
        self.first_line: bool = weight_max.first_line
        self.fake_limit: int = weight_max.fake_limit
        self.nobles_limit: int = weight_max.nobles_limit
        self.distance: float = 0
        self.night_bool: int = 0
        self.morale: int = 0
        self.initial_outline_minimum_noble_troops: int = (
            outline.initial_outline_minimum_noble_troops
        )

    def __eq__(self, other: Self) -> bool:
        return self.pk == other.pk

    def __hash__(self) -> int:
        return hash(self.pk)

    @property
    def nobles_allowed_to_use(self) -> int:
        if self.initial_outline_minimum_noble_troops == 0:
            possible_nobles_by_min_off = self.nobleman_left
        else:
            possible_nobles_by_min_off = (
                self.off_left // self.initial_outline_minimum_noble_troops
            )
        return min(self.nobleman_left, self.nobles_limit, possible_nobles_by_min_off)
