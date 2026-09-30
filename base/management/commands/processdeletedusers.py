# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from base.management.commands.utils import job_logs_and_metrics

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete users marked as deleted after expire time"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        expired = User.objects.filter(
            is_active=True,
            profile__deleted_at_exp__lt=timezone.now(),
        )
        deleted = expired.delete()
        log.info(deleted)
