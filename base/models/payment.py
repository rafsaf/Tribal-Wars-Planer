# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import secrets

from babel.numbers import format_currency
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy

from tribal_wars_planer.fetch_error_manager import FetchErrorManager


def promotion_event_id() -> str:
    unique_id = secrets.token_urlsafe(64)
    return f"promotion_{unique_id}"


class Payment(models.Model):
    """Represents real payment, only superuser access"""

    STATUS = [
        ("finished", gettext_lazy("Finished")),
        ("returned", gettext_lazy("Returned")),
    ]
    currency = models.CharField(
        max_length=3, default="PLN", choices=settings.SUPPORTED_CURRENCIES_CHOICES
    )
    status = models.CharField(max_length=30, choices=STATUS, default="finished")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    send_mail = models.BooleanField(default=True)
    mail_sent = models.BooleanField(default=False)
    amount = models.FloatField()
    exchange_rate = models.FloatField(default=None, null=True, blank=True)
    amount_pln = models.FloatField(default=0, blank=True)
    fee_pln = models.FloatField(default=0, blank=True)
    payment_intent_id = models.CharField(default="", max_length=512, blank=True)
    event_id = models.CharField(max_length=300, unique=True)
    from_stripe = models.BooleanField(default=False)
    promotion = models.BooleanField(default=False)
    language = models.CharField(
        max_length=16, default=settings.LANGUAGE_CODE, choices=settings.LANGUAGES
    )
    payment_date = models.DateField()
    months = models.IntegerField(default=1)
    comment = models.CharField(max_length=150, default="", blank=True)
    new_date = models.DateField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FetchErrorManager()

    def value(self) -> str:
        """Return human readable amount"""

        currency = self.currency.upper()

        if currency in settings.ZERO_DECIMAL_CURRENCIES:
            major_unit_amount = self.amount * 100.0
        else:
            major_unit_amount = self.amount

        translation.activate(self.language)
        language = translation.get_language() or "pl-pl"
        locale = language.replace("-", "_")

        return format_currency(
            major_unit_amount,
            currency,
            locale=locale,
        )

    def save(self, *args, **kwargs) -> None:
        if self.promotion:
            if not self.event_id:
                self.event_id = promotion_event_id()
        return super().save(*args, **kwargs)
