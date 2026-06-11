# Copyright 2026 Rafał Safin (rafsaf). All Rights Reserved.
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

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from base.management.commands.utils import job_logs_and_metrics

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete inactive users older than 24 hours"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        expiration_date = now() - timedelta(hours=24)
        expired = User.objects.filter(is_active=False, date_joined__lt=expiration_date)
        deleted = expired.delete()
        log.info(deleted)
