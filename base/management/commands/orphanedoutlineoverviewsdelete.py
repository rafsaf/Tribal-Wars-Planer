# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging

from django.core.management.base import BaseCommand
from django.db.models import Count

from base.management.commands.utils import job_logs_and_metrics
from base.models import OutlineOverview

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete orphaned outlineoverview without outline and links"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        orphaned = (
            OutlineOverview.objects.filter(outline=None)
            .annotate(num_of_overviews=Count("overview"))
            .filter(num_of_overviews=0)
        )
        deleted = orphaned.delete()
        log.info(deleted)
