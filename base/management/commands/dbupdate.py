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

from django.core.management.base import BaseCommand

from base.management.commands.decorators import job_logs_and_metrics
from base.models import World
from utils.database_update import WorldQuery

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update all Tribe, VillageModel, Player instances"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        worlds = []
        for world in World.objects.select_related("server").exclude(postfix="Test"):
            instance = WorldQuery(world=world)
            instance.update_all()
            worlds.append(world)
            message = (
                f"{str(world)} | tribe_updated: {instance.tribe_log_msg} |"
                f" village_update: {instance.village_log_msg} |"
                f" player_update: {instance.player_log_msg}"
            )
            log.info(message)
            self.stdout.write(self.style.SUCCESS(message))

        World.objects.bulk_update(
            worlds, ["last_update", "etag_player", "etag_tribe", "etag_village"]
        )
