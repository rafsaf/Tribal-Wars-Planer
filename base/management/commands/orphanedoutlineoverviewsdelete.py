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
