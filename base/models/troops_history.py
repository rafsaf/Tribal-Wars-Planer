# Copyright 2022 Rafał Safin (rafsaf). All Rights Reserved.
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

from base.models.outline import Outline


class TroopsHistory(models.Model):
    """Represent changes in outline off troops

    history_json can look like that, coord -> list of next versions of line

    {"500|500": [
            "342|530,0,0,2651,0,0,1031,0,0,274,0,0,0,0,",
            "342|530,0,0,261,0,0,101,0,0,24,0,0,0,0,"
        ]
    }
    """

    outline = models.OneToOneField(Outline, on_delete=models.CASCADE)
    history_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Troops History"
        verbose_name_plural = "Troops Histories"
