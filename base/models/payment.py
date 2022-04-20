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

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy


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
    amount = models.FloatField()
    exchange_rate = models.FloatField(default=None, null=True, blank=True)
    amount_pln = models.FloatField(default=0, blank=True)
    fee_pln = models.FloatField(default=0, blank=True)
    payment_intent_id = models.CharField(default="", max_length=512, blank=True)
    event_id = models.CharField(max_length=300, null=True, default=None, blank=True)
    from_stripe = models.BooleanField(default=False)
    payment_date = models.DateField()
    months = models.IntegerField(default=1)
    comment = models.CharField(max_length=150, default="", blank=True)
    new_date = models.DateField(default=None, null=True, blank=True)

    def value(self) -> str:
        return f"{self.amount} {self.currency}"
