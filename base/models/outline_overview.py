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

import typing

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from base.models.outline import Outline

if typing.TYPE_CHECKING:
    from base.models.overview import Overview


class OutlineOverview(models.Model):
    outline = models.ForeignKey(
        Outline, on_delete=models.SET_NULL, null=True, blank=True
    )
    weights_json = models.TextField(default="", blank=True)
    targets_json = models.TextField(default="", blank=True)
    world_json = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)
    outline_json = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)

    if typing.TYPE_CHECKING:
        overview_set: models.Manager[Overview]
