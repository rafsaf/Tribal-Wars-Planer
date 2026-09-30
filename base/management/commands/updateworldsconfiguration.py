# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging
from time import sleep

from django.core.management.base import BaseCommand
from django.db.models import Q

from base.management.commands.utils import job_logs_and_metrics
from base.models import World
from utils import database_update
from utils.database_update import WorldUpdateHandler

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update config of db worlds"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        db_worlds = World.objects.select_related("server").exclude(
            Q(postfix="Test") | Q(pending_delete=True)
        )

        for db_world in db_worlds:
            world_handler = WorldUpdateHandler(world=db_world)
            try:
                world_handler.create_or_update_config()
            except database_update.WorldOutdatedError as err:
                log.warning("world %s is outdated: %s", db_world, err)
                continue
            except database_update.DatabaseUpdateError as err:
                log.error("failed to update world %s: %s", db_world, err)
                continue
            log.info("updated world configuration %s", db_world)
            sleep(0.2)
