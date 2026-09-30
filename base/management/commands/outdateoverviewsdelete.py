# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from base.management.commands.utils import job_logs_and_metrics
from base.models import Overview

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete expired overview links"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        expiration_date = now() - timedelta(days=30)
        expired = Overview.objects.filter(created__lt=expiration_date)
        deleted = expired.delete()
        log.info(deleted)
