# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from base.management.commands.utils import job_logs_and_metrics
from base.views import analytics

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Refresh cached Plausible public script"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--force", action="store_true")

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        if not settings.PLAUSIBLE_DOMAIN or not settings.PLAUSIBLE_SCRIPT_PATH:
            log.info("Plausible script refresh skipped because analytics is disabled")
            return

        cached_payload = analytics.get_cached_plausible_script()

        try:
            refreshed = analytics.refresh_plausible_script_cache(
                force=options["force"],
            )
        except requests.RequestException as error:
            if cached_payload is not None:
                log.warning(
                    "Unable to refresh Plausible script, keeping stale cached version: %s",
                    error,
                )
                self.stdout.write(
                    "Unable to refresh Plausible script; keeping stale cached version"
                )
                return
            raise

        if refreshed:
            self.stdout.write(self.style.SUCCESS("Refreshed cached Plausible script"))
            return

        self.stdout.write(self.style.SUCCESS("Cached Plausible script is still fresh"))
