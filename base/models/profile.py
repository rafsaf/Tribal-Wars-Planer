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
from typing import TYPE_CHECKING
from django.utils.translation import gettext_lazy
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

if TYPE_CHECKING:
    from base.models import Message
from base.models.server import Server


class Profile(models.Model):

    INPUT_DATA_TYPES = [
        ("Army collection", gettext_lazy("Army collection")),
        ("Deff collection", gettext_lazy("Deff collection")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    server = models.ForeignKey(
        Server, on_delete=models.SET_NULL, null=True, default=None
    )
    validity_date = models.DateField(
        default=datetime.date(year=2021, month=2, day=25), blank=True, null=True
    )
    currency = models.CharField(
        max_length=3, default="PLN", choices=settings.SUPPORTED_CURRENCIES_CHOICES
    )
    messages = models.IntegerField(default=0)
    server_bind = models.BooleanField(default=False)
    default_morale_on = models.BooleanField(default=False)
    input_data_type = models.CharField(
        max_length=32, default="Army collection", choices=INPUT_DATA_TYPES
    )

    def is_premium(self) -> bool:
        if settings.PREMIUM_ACCOUNT_VALIDATION_ON:
            if self.validity_date is None:
                return False
            today = timezone.localdate()
            if today > self.validity_date:
                return False
            return True
        return True

    def latest_messages(self) -> QuerySet["Message"]:
        from base.models.message import Message

        return Message.objects.order_by("-created")[:6]
