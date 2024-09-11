# Copyright 2024 Rafał Safin (rafsaf). All Rights Reserved.
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

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from base.models.outline import Outline
from utils.outline_complete import complete_outline_write

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Debug complete outline"

    def handle(self, *args, **options):
        pk: int = options["outline_pk"]

        outline = Outline.objects.select_related().get(pk=pk)
        with transaction.atomic():
            complete_outline_write(outline=outline)
            outline.actions.click_outline_write(outline)
            outline.written = "active"
            outline.save()

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("outline_pk", type=int)
        return super().add_arguments(parser)
