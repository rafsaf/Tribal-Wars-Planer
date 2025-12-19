# Copyright 2025 Rafał Safin (rafsaf). All Rights Reserved.
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

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models.overview import Overview
from base.models.world import World


class Shipment(models.Model):
    name = models.CharField(max_length=24)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    overviews = models.ManyToManyField(Overview, blank=True)
    sent_lst = ArrayField(models.BigIntegerField(), blank=True, default=list)
    hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
