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

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from base.management.commands.utils import job_logs_and_metrics
from base.models import Overview

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete expired overview links"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        expiration_date = now() - timedelta(days=30)
        expired = Overview.objects.filter(created__lt=expiration_date)
        expired.delete()
