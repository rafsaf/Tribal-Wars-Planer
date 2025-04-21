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

from base.models.outline import Outline
from utils.available_troops import calculate_and_update_available_troops

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Debug calculate_and_update_available_troops"

    def handle(self, *args, **options) -> None:
        pk: int = options["outline_pk"]

        outline = Outline.objects.select_related().get(pk=pk)
        calculate_and_update_available_troops(outline=outline)

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("outline_pk", type=int)
        return super().add_arguments(parser)
