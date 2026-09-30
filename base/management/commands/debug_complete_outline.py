# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from base.models.outline import Outline
from utils.outline_complete import complete_outline_write

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Debug complete outline"

    def handle(self, *args, **options):
        pk: int = options["outline_pk"]

        outline = Outline.objects.select_related("world").get(pk=pk)
        with transaction.atomic():
            complete_outline_write(outline=outline)
            outline.actions.click_outline_write(outline)
            outline.written = "active"
            outline.save(update_fields=["written"])

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("outline_pk", type=int)
        return super().add_arguments(parser)
