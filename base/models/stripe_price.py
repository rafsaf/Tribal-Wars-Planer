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

from django.conf import settings
from django.db import models


class StripePrice(models.Model):
    price_id = models.CharField(max_length=128, primary_key=True)
    product = models.ForeignKey("StripeProduct", on_delete=models.CASCADE)
    active = models.BooleanField()
    created = models.IntegerField()
    amount = models.IntegerField()
    currency = models.CharField(
        max_length=3, choices=settings.SUPPORTED_CURRENCIES_CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["amount", "currency"], name="unique price")
        ]
        ordering = ["currency", "-active", "amount"]

    def get_amount(self) -> float:
        """Return human readable amount"""
        return self.amount / 100
