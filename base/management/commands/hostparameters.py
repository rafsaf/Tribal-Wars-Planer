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

import psutil
from django.core.management.base import BaseCommand

import metrics

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Get host parameters"

    def handle(self, *args, **options):
        metrics.CPU.set(psutil.cpu_percent())
        metrics.MEMORY.set(psutil.virtual_memory().percent)
        metrics.DISK.set(psutil.disk_usage("/").percent)
