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


import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from otp_yubikey.models import ValidationService

from base.management.commands.utils import job_logs_and_metrics

log = logging.getLogger(__name__)


class Command(BaseCommand):  # pragma: no cover
    help = "Init 2fa"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        ValidationService.objects.get_or_create(
            name="default",
            use_ssl=True,
            param_sl="",
            param_timeout="",
            defaults={
                "api_id": settings.YUBICO_VALIDATION_SERVICE_API_ID,
                "api_key": settings.YUBICO_VALIDATION_SERVICE_API_KEY,
            },
        )
