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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class StripeProduct(models.Model):
    product_id = models.CharField(max_length=128, primary_key=True)
    active = models.BooleanField()
    name = models.CharField(max_length=512)
    updated = models.IntegerField()
    created = models.IntegerField()
    months = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )

    class Meta:
        ordering = ["-active", "months"]

    def __str__(self) -> str:
        if self.months == 1:
            return _("Premium 1 month")
        else:
            return _("Premium %s months") % self.months
