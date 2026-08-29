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

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from base.management.commands.utils import job_logs_and_metrics

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete users marked as deleted after expire time"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        expired = User.objects.filter(
            is_active=True,
            profile__deleted_at_exp__lt=timezone.now(),
        )
        deleted = expired.delete()
        log.info(deleted)
