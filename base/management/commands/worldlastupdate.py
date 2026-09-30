# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging
import time

from django.core.management.base import BaseCommand

import metrics
from base.management.commands.utils import job_logs_and_metrics
from base.models import World

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Get worlds last update time delay"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        worlds = World.objects.select_related("server").exclude(postfix="Test")
        now = int(time.time())
        for world in worlds:
            metrics.WORLD_LAST_UPDATE.labels(world=str(world)).set(
                now - int(world.last_modified_timestamp())
            )
