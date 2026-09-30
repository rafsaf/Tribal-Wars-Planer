# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

import metrics
from base.management.commands.utils import job_logs_and_metrics
from base.models import Server

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates servers objects in database"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        metrics.CRONTASK.labels("createservers").inc()
        server_info: tuple[str, str, str]
        for server_info in settings.TRIBAL_WARS_SUPPORTED_SERVERS:
            server, created = Server.objects.get_or_create(
                dns=server_info[0],
                defaults={"prefix": server_info[1], "tz": server_info[2]},
            )
            save = False
            if server.prefix != server_info[1]:
                server.prefix = server_info[1]
                save = True
            if str(server.tz) != server_info[2]:
                server.tz = server_info[2]
                save = True
            if save:
                self.stdout.write(
                    self.style.SUCCESS(f"Updated: Server: {server_info[0]}")
                )
                server.save()

            self.stdout.write(
                self.style.SUCCESS(f"Created: {created}, Server: {server_info[0]}")
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Success, {len(settings.TRIBAL_WARS_SUPPORTED_SERVERS)} TW servers"
            )
        )
