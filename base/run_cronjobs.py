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

""" Cronjobs runner"""
import logging
import sys
import threading
from time import sleep
from typing import Callable

import schedule
from django import setup
from django.conf import settings


def run_threaded(job_func: Callable):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == "__main__":
    try:
        setup()
        logging.info("Cronjobs starting")
        from base.cron import (
            db_update,
            outdate_outline_delete,
            outdate_overviews_delete,
        )

        schedule.every(settings.JOB_MIN_INTERVAL).to(
            settings.JOB_MAX_INTERVAL
        ).minutes.do(run_threaded, db_update)
        schedule.every().hour.do(run_threaded, outdate_overviews_delete)
        schedule.every().hour.do(run_threaded, outdate_outline_delete)
    except Exception as err:
        logging.error(err)
        raise Exception(err)

    db_update()  # extra db_update on startup

    secs_lifetime: int = settings.JOB_LIFETIME_MAX_SECS
    rounds = secs_lifetime / 5
    while True:
        schedule.run_pending()
        sleep(5)
        if secs_lifetime:
            if rounds < 0:
                break
            rounds -= 1

    logging.info("Cronjobs restarting in 60s...")
    sleep(60)  # grace period 60s waiting for threads end
    sys.exit(0)
