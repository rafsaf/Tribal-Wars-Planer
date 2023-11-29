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

import datetime

from django.db import models
from django.utils.translation import gettext_lazy

from base.models.outline_time import OutlineTime


class PeriodModel(models.Model):
    """Handle one period of time in outline specification"""

    STATUS: list[tuple[str, str]] = [
        ("all", gettext_lazy("All")),
        ("random", gettext_lazy("Random")),
        ("exact", gettext_lazy("Exact")),
    ]
    UNITS: list[tuple[str, str]] = [
        ("noble", gettext_lazy("Noble")),
        ("ram", gettext_lazy("Ram")),
    ]
    outline_time = models.ForeignKey(OutlineTime, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS)
    unit = models.CharField(max_length=15, choices=UNITS)
    from_number = models.IntegerField(null=True, default=None, blank=True)
    to_number = models.IntegerField(null=True, default=None, blank=True)
    from_time = models.TimeField(default=datetime.time(hour=7))
    to_time = models.TimeField(default=datetime.time(hour=7))
