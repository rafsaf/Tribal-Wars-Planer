# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
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

""" Cronjobs """
from datetime import timedelta
from time import sleep

from django.db.models.query import QuerySet
from django.utils.timezone import now

from utils.database_update import cron_schedule_data_update
from utils.logger import cron_log

from . import models


def db_update():
    """Database update"""
    cron_log.info("Start db_update")
    cron_schedule_data_update()


def outdate_overviews_delete():
    """Delete expired links"""
    cron_log.info("Start outdate_overviews_delete")
    expiration_date = now() - timedelta(days=30)
    expired = models.Overview.objects.filter(created__lt=expiration_date)
    expired.delete()


def outdate_outline_delete(days: int = 35) -> None:
    """Delete outlines older than 35 days except test World"""
    cron_log.info("Start outdate_outline_delete")
    expiration_date = now() - timedelta(days=days)
    expired: "QuerySet[models.Outline]" = (
        models.Outline.objects.select_related("world")
        .filter(created__lt=expiration_date)
        .exclude(world__postfix="Test")
    )
    outline: models.Outline
    for outline in expired:
        outline.delete()
        sleep(0.2)
