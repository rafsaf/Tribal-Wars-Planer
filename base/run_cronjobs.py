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

import threading
from time import sleep
from typing import Callable

import schedule
from django import setup


def run_threaded(job_func: Callable):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == "__main__":
    setup()
    from base.cron import db_update, outdate_outline_delete, outdate_overviews_delete

    schedule.every(15).minutes.do(run_threaded, db_update)
    schedule.every().hour.do(run_threaded, outdate_overviews_delete)
    schedule.every().hour.do(run_threaded, outdate_outline_delete)
    while True:
        schedule.run_pending()
        sleep(5)
