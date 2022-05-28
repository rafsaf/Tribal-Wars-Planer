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
