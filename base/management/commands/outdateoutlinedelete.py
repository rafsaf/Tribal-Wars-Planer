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
from datetime import timedelta
from time import sleep

from django.core.management.base import BaseCommand
from django.db.models.query import QuerySet
from django.utils.timezone import now

import metrics
from base.models import Outline

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete outlines older than 35 days except test World"

    def handle(self, *args, **options):
        log.info("job:outdateoutlinedelete start")
        self.stdout.write(self.style.SUCCESS("job:outdateoutlinedelete start"))
        try:
            expiration_date = now() - timedelta(days=35)
            expired: QuerySet[Outline] = (
                Outline.objects.select_related("world")
                .filter(created__lt=expiration_date)
                .exclude(world__postfix="Test")
            )
            for outline in expired:
                outline.delete()
                sleep(0.2)
        except Exception as error:
            log.error(f"job:outdateoutlinedelete error: {error}")
            metrics.ERRORS.labels("job:outdateoutlinedelete").inc()
        self.stdout.write(self.style.SUCCESS("job:outdateoutlinedelete success"))
