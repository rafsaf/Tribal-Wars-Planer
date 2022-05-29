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

from base import models
from utils import basic


class TargetsData:
    def __init__(self, data: str, world: models.World):
        """
        Param data is text input data saved by user
        """
        self.world = world
        self.data = data
        self.lines = data.split("\r\n")
        self.villages_coord = []
        self.vill_id_line = {}
        self.errors_ids = set()
        self.new_validated_data = ""

    def validate(self):
        for i, line in enumerate(self.lines):
            try:
                validated = TargetsOneLine(line).validate_line()
            except LineError:
                # this line will be red - with error
                self.errors_ids.add(i)
            else:
                # line is correct
                self.villages_coord.append(validated[0])
                self.vill_id_line[validated[0]] = i
                self.new_validated_data += validated[1] + "\r\n"

        self.validate_villages_database()

    def validate_villages_database(self):
        village_models = (
            models.VillageModel.objects.select_related()
            .filter(world=self.world, coord__in=self.villages_coord)
            .exclude(player=None)
        )

        if len(set(self.villages_coord)) != village_models.count():
            villages_ids_set = {village.coord for village in village_models}

            for village in self.villages_coord:
                if village not in villages_ids_set:
                    self.errors_ids.add(self.vill_id_line[village])


class LineError(Exception):
    """Represents an error in line like '000|000:5:5'"""


class TargetsOneLine:
    """Represent one target line like '000|000:5:5' or '000|000'"""

    def __init__(self, line: str):
        self.line = line

    def validate_line(self):
        """Raise exception when line is incorrect, None when line is a separator, (coord, line) else"""
        split_line = self.line.split(":")

        # too much data
        if len(split_line) > 3:
            raise LineError()

        # first (only) match is not proper village coord
        try:
            coord = split_line[0]
            if len(coord) != 7:
                raise basic.VillageError()
            basic.Village(coord)
        except basic.VillageError:
            raise LineError()

        # rest two matches are not integers
        if len(split_line) == 3:
            if not self.split_is_valid(split_line[1]) or not self.split_is_valid(
                split_line[2]
            ):
                raise LineError()

        # only one match after coord
        if len(split_line) == 2:
            if not self.split_is_valid(split_line[1]):
                raise LineError()
            self.line += ":0"

        # only coord
        if len(split_line) == 1:
            self.line += ":0:0"

        return (coord, self.line)

    def split_is_valid(self, split_line: str):
        # valids are numeric and 0|0|0|0 only
        if split_line.isnumeric():
            return True

        new = split_line.split("|")
        if len(new) != 4:
            return False
        for item in new:
            if not item.isnumeric():
                return False
        return True
