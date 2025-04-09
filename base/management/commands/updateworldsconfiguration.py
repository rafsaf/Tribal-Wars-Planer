# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
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
from time import sleep

from django.core.management.base import BaseCommand
from django.db import transaction

from base.management.commands.utils import job_logs_and_metrics
from base.models import World
from utils.database_update import WorldUpdateHandler

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update config of db worlds"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        db_worlds = World.objects.exclude(postfix="Test")

        for db_world in db_worlds:
            with transaction.atomic():
                world = World.objects.select_for_update().get(pk=db_world.pk)
                world_handler = WorldUpdateHandler(world=world)
                success = world_handler.create_or_update_config()
                if not success:
                    log.error("failed to update world %s", world)
                log.info("world %s configuration up to date", db_world)
            log.info("updated world configuration %s", db_world)
            sleep(0.2)
