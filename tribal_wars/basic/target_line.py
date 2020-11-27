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
        self.village_ids = []
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
                    coord = validated[0]
                    village_id = f"{ coord[0:3] }{ coord[4:7] }{ self.world }"
                    self.village_ids.append(village_id)
                    self.vill_id_line[village_id] = i
                    self.new_validated_data += validated[1] + "\r\n"

        self.validate_villages_database()

        if self.division_count == 0:
            self.new_validated_data += "---"

    def validate_villages_database(self):
        village_models = models.VillageModel.objects.filter(
            id__in=self.village_ids)

        if len(self.village_ids) != village_models.count():
            villages_ids_set = set(self.village_ids)

            for village in village_models:
                if not village.pk in villages_ids_set:
                    self.errors_ids.add(self.vill_id_line[village.pk])


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

