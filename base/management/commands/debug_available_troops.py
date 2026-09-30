# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging

from django.core.management.base import BaseCommand, CommandParser

from base.models.outline import Outline
from utils.available_troops import calculate_and_update_available_troops

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Debug calculate_and_update_available_troops"

    def handle(self, *args, **options) -> None:
        pk: int = options["outline_pk"]

        outline = Outline.objects.select_related("world").get(pk=pk)
        calculate_and_update_available_troops(outline=outline)

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("outline_pk", type=int)
        return super().add_arguments(parser)
