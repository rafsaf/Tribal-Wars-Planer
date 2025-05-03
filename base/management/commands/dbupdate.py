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
from concurrent import futures

from django.conf import settings
from django.core.management.base import BaseCommand

import metrics
from base.management.commands.utils import job_logs_and_metrics
from base.models import World
from base.models.outline import Outline
from utils.database_update import WorldUpdateHandler

log = logging.getLogger(__name__)


def update_world(world: World, command: BaseCommand):
    try:
        world_handler = WorldUpdateHandler(world=world)
        have_outlines = Outline.objects.filter(world=world).exists()
        if have_outlines:
            download_try = settings.WORLD_UPDATE_TRY_COUNT
        else:
            download_try = 1
        message = world_handler.update_all(download_try=download_try)
        command.stdout.write(command.style.SUCCESS(message))
        log.info(message)
    except Exception as error:
        log.error("error in task dbupdate %s: %s", world, error, exc_info=True)
        metrics.ERRORS.labels(f"task_dbupdate {world}").inc()


class Command(BaseCommand):
    help = "Update all Tribe, VillageModel, Player instances"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        worlds = list(World.objects.select_related("server").exclude(postfix="Test"))

        with futures.ThreadPoolExecutor(
            max_workers=settings.WORLD_UPDATE_THREADS
        ) as executor:
            tasks: list[futures.Future] = []
            for world in worlds:
                log.info("submited update_world task for world: %s to executor", world)
                tasks.append(executor.submit(update_world, world=world, command=self))

            futures.wait(tasks)
