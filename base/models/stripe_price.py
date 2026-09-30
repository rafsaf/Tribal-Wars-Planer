# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from babel.numbers import format_currency
from django.conf import settings
from django.db import models
from django.utils import translation

from base.models.stripe_product import StripeProduct
from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class StripePrice(models.Model):
    price_id = models.CharField(max_length=128, primary_key=True)
    product = models.ForeignKey(StripeProduct, on_delete=models.CASCADE)
    active = models.BooleanField()
    created = models.IntegerField()
    amount = models.IntegerField()
    currency = models.CharField(
        max_length=3, choices=settings.SUPPORTED_CURRENCIES_CHOICES
    )

    objects = FetchErrorManager()

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
