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

from django.db import models


class Stats(models.Model):
    outline = models.ForeignKey(
        "Outline", on_delete=models.SET_NULL, null=True, blank=True
    )
    outline_pk = models.IntegerField()
    owner_name = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    world = models.CharField(max_length=50)
    premium_user = models.BooleanField()
    off_troops = models.IntegerField(default=0)
    deff_troops = models.IntegerField(default=0)
    real_targets = models.IntegerField(default=0)
    fake_targets = models.IntegerField(default=0)
    ruin_targets = models.IntegerField(default=0)
    troops_refreshed = models.IntegerField(default=0)
    outline_written = models.IntegerField(default=0)
    available_troops = models.IntegerField(default=0)
    date_change = models.IntegerField(default=0)
    settings_change = models.IntegerField(default=0)
    night_change = models.IntegerField(default=0)
    ruin_change = models.IntegerField(default=0)
    building_order_change = models.IntegerField(default=0)
    time_created = models.IntegerField(default=0)
    go_back_clicked = models.IntegerField(default=0)
    finish_outline_clicked = models.IntegerField(default=0)
    overview_visited = models.IntegerField(default=0)
