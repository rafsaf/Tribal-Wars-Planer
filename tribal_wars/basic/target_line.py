from django.db.models import F, ExpressionWrapper, CharField
from django.db.models.functions import Cast, Concat

from base import models
from tribal_wars import basic


class TargetsData:
    def __init__(self, data: str, world: int):
        """
        Param data is text input data saved by user
        """
        self.world = world
        self.data = data
        self.lines = data.split("\r\n")
        self.division_count = 0
        self.villages_coord = []
        self.vill_id_line = {}
        self.errors_ids = set()
        self.new_validated_data = str()

    def validate(self):
        for i, line in enumerate(self.lines):
            try:
                validated = TargetsOneLine(line).validate_line()
            except SeparateLineException:
                # this line will be red - with error
                self.errors_ids.add(i)
            else:
                if validated is None:
                    # line is separator
                    self.division_count += 1
                    self.new_validated_data +=  "---\r\n"
                    if self.division_count > 1:
                        # too much separators
                        self.errors_ids.add(i)

                else:
                    # line is correct
                    self.villages_coord.append(validated[0])
                    self.vill_id_line[validated[0]] = i
                    self.new_validated_data += validated[1] + "\r\n"

        self.validate_villages_database()

        if self.division_count == 0:
            self.new_validated_data += "---"

    def validate_villages_database(self):
        village_models = models.VillageModel.objects.select_related().filter(world=self.world, coord__in=self.villages_coord)

        if len(self.villages_coord) != village_models.count():
            villages_ids_set = set(self.villages_coord)

            for village in village_models:
                if not village.coord in villages_ids_set:
                    self.errors_ids.add(self.vill_id_line[village.coord])


class SeparateLineException(Exception):
    pass


class TargetsOneLine:
    """ Represent one target line like '000|000:5:5' or '000|000' """

    def __init__(self, line: str):
        self.line = line

    def validate_line(self):
        """ Raise exception when line is incorrect, None when line is a separator, (coord, line) else """

        # check if line is separator
        if self.line == "---":
            return None

        split_line = self.line.split(":")

        # too much data
        if len(split_line) > 3:
            raise SeparateLineException()

        # first (only) match is not proper village coord
        try:
            coord = split_line[0]
            if len(coord) != 7:
                raise basic.VillageError()
            village = basic.Village(coord)
        except basic.VillageError:
            raise SeparateLineException()

        # rest two matches are not integers
        if len(split_line) == 3:
            if not self.split_is_valid(split_line[1]) or not self.split_is_valid(split_line[2]):
                raise SeparateLineException()

        # only one match after coord
        if len(split_line) == 2:
            if not self.split_is_valid(split_line[1]):
                raise SeparateLineException
            self.line += ':0'

        # only coord
        if len(split_line) == 1:
            self.line += ':0:0'

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

