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
import signal
import threading
from types import FrameType

import schedule
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

import metrics
from base.management.commands.utils import run_threaded

log = logging.getLogger(__name__)
exit_event = threading.Event()


def quit(sig: int, frame: FrameType | None) -> None:
    log.info("interrupted by %s, shutting down", sig)
    exit_event.set()


class Command(BaseCommand):
    help = "Cronjobs runner"

    def handle(self, *args, **options) -> None:
        log.info("task runcronjobs start")
        try:
            signal.signal(signalnum=signal.SIGINT, handler=quit)
            signal.signal(signalnum=signal.SIGTERM, handler=quit)

            schedule.every(settings.JOB_MIN_INTERVAL).to(
                settings.JOB_MAX_INTERVAL
            ).seconds.do(run_threaded, call_command, command_name="dbupdate")
            schedule.every(5).seconds.do(
                run_threaded,
                call_command,
                command_name="outdateoverviewsdelete",
            )
            schedule.every(5).seconds.do(
                run_threaded,
                call_command,
                command_name="outdateoutlinedelete",
            )
            schedule.every(5).seconds.do(
                run_threaded,
                call_command,
                command_name="calculatepaymentfee",
            )
            schedule.every(5).seconds.do(
                run_threaded,
                call_command,
                command_name="hostparameters",
            )
            schedule.every(60).to(120).seconds.do(
                run_threaded,
                call_command,
                command_name="worldlastupdate",
            )
            if settings.WORLD_UPDATE_FETCH_ALL:
                schedule.every(5).to(7).hours.do(
                    run_threaded,
                    call_command,
                    command_name="fetchnewworlds",
                )

            call_command("dbupdate")  # extra db_update on startup

            while not exit_event.is_set():
                schedule.run_pending()
                exit_event.wait(5)

        except Exception as error:
            msg = f"task runcronjobs failed: {error}"
            self.stdout.write(self.style.ERROR(msg))
            log.error(msg)
            metrics.ERRORS.labels("task_runcronjobs").inc()
