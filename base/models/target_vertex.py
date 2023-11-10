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

from typing import TYPE_CHECKING

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.urls import reverse
from django.utils.translation import gettext_lazy

from base.models.outline import Outline
from base.models.outline_time import OutlineTime


class TargetVertex(models.Model):
    """Target Village"""

    MODE_OFF = [
        ("closest", gettext_lazy("Closest Front")),
        ("close", gettext_lazy("Close Back")),
        ("random", gettext_lazy("Random Back")),
        ("far", gettext_lazy("Far Back")),
    ]

    MODE_NOBLE = [
        ("closest", gettext_lazy("Closest Front")),
        ("close", gettext_lazy("Close Back")),
        ("random", gettext_lazy("Random Back")),
        ("far", gettext_lazy("Far Back")),
    ]

    MODE_DIVISION = [
        ("divide", gettext_lazy("Divide off with nobles")),
        ("not_divide", gettext_lazy("Dont't divide off")),
        ("separatly", gettext_lazy("Off and nobles separatly")),
    ]

    NOBLE_GUIDELINES = [
        ("one", gettext_lazy("Try send all nobles to one target")),
        ("many", gettext_lazy("Nobles to one or many targets")),
        ("single", gettext_lazy("Try single nobles from many villages")),
    ]

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE, db_index=True)
    outline_time = models.ForeignKey(
        OutlineTime, on_delete=models.SET_NULL, null=True, default=None
    )
    target = models.CharField(max_length=7)
    player = models.CharField(max_length=30)
    player_created_at = models.DateTimeField(default=now)
    points = models.IntegerField(default=0)
    fake = models.BooleanField(default=False)
    ruin = models.BooleanField(default=False)

    required_off = models.IntegerField(default=0)
    required_noble = models.IntegerField(default=0)

    exact_off = ArrayField(models.IntegerField(), default=list, size=4)
    exact_noble = ArrayField(models.IntegerField(), default=list, size=4)

    mode_off = models.CharField(max_length=15, choices=MODE_OFF, default="random")
    mode_noble = models.CharField(max_length=15, choices=MODE_NOBLE, default="closest")
    mode_division = models.CharField(
        max_length=15, choices=MODE_DIVISION, default="not_divide"
    )
    mode_guide = models.CharField(
        max_length=15, choices=NOBLE_GUIDELINES, default="one"
    )
    night_bonus = models.BooleanField(default=False)
    enter_t1 = models.IntegerField(default=7)
    enter_t2 = models.IntegerField(default=12)

    if TYPE_CHECKING:
        from base.models.weight_model import WeightModel

        weightmodel_set: QuerySet[WeightModel]

    class Meta:
        verbose_name = "Target"
        verbose_name_plural = "Targets"

    def __str__(self):
        return self.target

    def get_absolute_url(self):
        return reverse("base:planer_initial_detail", args=[self.outline.pk, self.pk])

    def coord_tuple(self):
        return (int(self.target[0:3]), int(self.target[4:7]))
