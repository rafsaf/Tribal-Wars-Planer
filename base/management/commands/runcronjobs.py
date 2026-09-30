# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
            ).minutes.do(run_threaded, call_command, command_name="dbupdate")
            schedule.every().hour.do(
                run_threaded, call_command, command_name="outdateoverviewsdelete"
            )
            schedule.every().hour.do(
                run_threaded, call_command, command_name="outdateoutlinedelete"
            )
            schedule.every().hour.do(
                run_threaded,
                call_command,
                command_name="orphanedoutlineoverviewsdelete",
            )
            schedule.every().hour.do(
                run_threaded, call_command, command_name="inactiveusersdelete"
            )
            schedule.every().hour.do(
                run_threaded, call_command, command_name="processdeletedusers"
            )
            schedule.every().hour.do(
                run_threaded,
                call_command,
                command_name="refreshplausiblescriptcache",
            )
            schedule.every(5).minutes.do(
                run_threaded, call_command, command_name="calculatepaymentfee"
            )
            schedule.every(60).to(120).seconds.do(
                run_threaded, call_command, command_name="worldlastupdate"
            )
            schedule.every(5).to(10).minutes.do(
                run_threaded, call_command, command_name="missedemailssend"
            )
            schedule.every(11).to(13).hours.do(
                run_threaded, call_command, command_name="updateworldsconfiguration"
            )
            if settings.WORLD_UPDATE_FETCH_ALL:
                schedule.every(5).to(7).hours.do(
                    run_threaded, call_command, command_name="fetchnewworlds"
                )

            try:
                call_command("dbupdate")  # extra db_update on startup
            except Exception as error:
                log.warning(
                    "startup dbupdate failed: %s",
                    error,
                )

            try:
                call_command("refreshplausiblescriptcache")
            except Exception as error:
                log.warning(
                    "startup refreshplausiblescriptcache failed, keeping existing cache: %s",
                    error,
                )

            while not exit_event.is_set():
                schedule.run_pending()
                exit_event.wait(5)

        except Exception as error:
            msg = f"task runcronjobs failed: {error}"
            self.stdout.write(self.style.ERROR(msg))
            log.error(msg)
            metrics.ERRORS.labels("task_runcronjobs").inc()
