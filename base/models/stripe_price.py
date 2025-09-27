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

from babel.numbers import format_currency
from django.conf import settings
from django.db import models
from django.utils import translation

from base.models.stripe_product import StripeProduct


class StripePrice(models.Model):
    price_id = models.CharField(max_length=128, primary_key=True)
    product = models.ForeignKey(StripeProduct, on_delete=models.CASCADE)
    active = models.BooleanField()
    created = models.IntegerField()
    amount = models.IntegerField()
    currency = models.CharField(
        max_length=3, choices=settings.SUPPORTED_CURRENCIES_CHOICES
    )

    class Meta:
        ordering = ["currency", "-active", "amount"]

    def get_amount(self) -> str:
        """Return human readable amount"""

        currency = self.currency.upper()

        if currency in settings.ZERO_DECIMAL_CURRENCIES:
            major_unit_amount = self.amount
        else:
            major_unit_amount = self.amount / 100.0

        language = translation.get_language() or "pl"
        locale = language.replace("-", "_")

        return format_currency(
            major_unit_amount,
            currency,
            locale=locale,
        )
