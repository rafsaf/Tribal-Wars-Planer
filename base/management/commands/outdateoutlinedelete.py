# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models.query import QuerySet
from django.utils.timezone import now

from base.management.commands.utils import job_logs_and_metrics
from base.models import Outline

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete outlines older than 35 days except test World"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        expiration_date = now() - timedelta(days=35)
        expired: QuerySet[Outline] = Outline.objects.select_related("world").filter(
            created__lt=expiration_date
        )
        deleted = expired.delete()
        log.info(deleted)
