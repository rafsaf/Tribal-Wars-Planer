# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
