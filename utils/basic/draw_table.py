# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
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

# The MIT License (MIT)

# Copyright (c) 2017 Andrea Peter

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
Simple table drawing library
"""

# default values are for reStructuredText grid tables (e.g. for sphinx)
HEADERS_ROW_SEP_CHAR = "="
ROW_SEP_CHAR = "-"
CORNER_CHAR = "+"
CELL_FILL_CHAR = " "
CELL_SEP_CHAR = "|"
DEFAULT_VALUE = "-"
NEWLINE = "\n"
MIN_H_PADDING = 1  # the minimum horizontal padding on each side of a cell value

SUPPORTED_NEWLINES = "\n \r \r\n".split(" ")


class SimpleTableError(ValueError):
    pass


class Table:
    def __init__(
        self,
        headers,
        data,
        row_sep_char=ROW_SEP_CHAR,
        headers_row_sep_char=HEADERS_ROW_SEP_CHAR,
        corner_char=CORNER_CHAR,
        cell_sep_char=CELL_SEP_CHAR,
        cell_fill_char=CELL_FILL_CHAR,
        min_h_padding=MIN_H_PADDING,
        column_keys=None,
        default_value=DEFAULT_VALUE,
        newline=NEWLINE,
    ):
        """
        For arguments documentation see the `py_draw_table()` function
        """
        self.headers = headers
        self.data = data
        self.row_sep_char = str(row_sep_char)
        self.header_row_sep_char = str(headers_row_sep_char)
        self.corner_char = str(corner_char)
        self.cell_sep_char = str(cell_sep_char)
        self.cell_fill_char = str(cell_fill_char)
        self.min_h_padding = int(min_h_padding)
        self.column_keys = column_keys
        self.default_value = str(default_value)
        self.newline = str(newline)

        if not self.data:
            raise SimpleTableError("No data received")

        for value in (
            row_sep_char,
            headers_row_sep_char,
            corner_char,
            cell_sep_char,
            cell_fill_char,
        ):
            if len(value) != 1:
                raise SimpleTableError(
                    f"Table structure parameters must have length 1: '{value}'"
                )

        self.min_h_padding = max(self.min_h_padding, 0)

        if self.newline not in SUPPORTED_NEWLINES:
            raise SimpleTableError(f"newline '{newline}' not supported")

        # if we got a list of dictionaries: make list of lists
        if self.column_keys is not None:
            if len(self.headers) != len(self.column_keys):
                raise SimpleTableError("headers and columns must have same length!")
            self.data = self._get_list_of_lists(self.data)

        self.column_widths = self.row_separator = self.header_row_separator = None

    def draw(self):
        self.column_widths = self._get_column_widths()
        self.row_separator = self._build_row_sep()
        self.header_row_separator = self._build_row_sep(
            row_sep_char=self.header_row_sep_char
        )

        return (
            "{row_sep}{newline}{header}{newline}{header_sep}{newline}{data_rows}"
        ).format(
            row_sep=self.row_separator,
            header=self._build_row(self.headers),
            header_sep=self.header_row_separator,
            data_rows=self.newline.join(
                [
                    self._build_row(row) + self.newline + self.row_separator
                    for row in self.data
                ]
            ),
            newline=self.newline,
        )

    def _split_cell_value(self, value):
        """Splits a given string in lines according to self.newline"""
        return str(value).split(self.newline)

    def _get_list_of_lists(self, data):
        """Transforms a list of dicts in list of lists through column_keys"""
        return [
            [
                row_dict.get(column_key, self.default_value)
                for column_key in self.column_keys  # type: ignore
            ]
            for row_dict in data
        ]

    def _get_column_widths(self):
        """
        Returns a list of column widths (in characters)
        :return: a list of integers representing the width of each row (in characters)
        """
        # getting width for table data
        column_widths = [0] * len(self.data[0])  # all zeroes
        for row in self.data:
            for column_index, cell_value in enumerate(row):
                # splitting cell in lines
                for line in self._split_cell_value(cell_value):
                    column_widths[column_index] = max(
                        column_widths[column_index],
                        len(str(line)) + self.min_h_padding * 2,
                    )

        # updating with width of headers, multi-line headers not supported!
        for col_index, header in enumerate(self.headers):
            column_widths[col_index] = max(
                column_widths[col_index], len(header) + self.min_h_padding * 2
            )

        return column_widths

    def _fill_h_cell_padding(self, cell_line, cell_width):
        """Returns the value with horizontal cell padding filled
        e.g.
        value = "miao", width = 10
        returns " miao     "
        assuming cell_fill_char is a whitespace and self.min_h_padding = 1
        :param cell_line: The a line of a cell value
        :param cell_width: The total length of the cell (in characters)
        :returns: string
        """
        cell_line = str(cell_line)
        assert len(cell_line) <= cell_width - (2 * self.min_h_padding)  # TODO
        return "{}{}{}".format(  # noqa: UP032
            # left padding: min_h_padding
            self.cell_fill_char * self.min_h_padding,
            # value
            cell_line,
            # right padding: the remaining space
            self.cell_fill_char * (cell_width - len(cell_line) - self.min_h_padding),
        )

    def _build_row_sep(self, row_sep_char=None):
        """Builds a row separator
        :param row_sep_char: the character that separates rows
        :returns: a row separator string
        """
        if row_sep_char is not None:
            assert len(row_sep_char) == 1, "row_sep_char must have length 1"
        else:
            row_sep_char = self.row_sep_char
        return "{}{}{}".format(
            self.corner_char,
            self.corner_char.join(
                [row_sep_char * min_col_length for min_col_length in self.column_widths]  # type: ignore
            ),
            self.corner_char,
        )

    def _build_row(self, row):
        """
        Builds a table row string
        :param row: a list containing the fields of the table row
        :returns: a table row string
        """
        assert len(row) > 0, "Row is empty"

        # first we split cell-values in a list of lines in order to support multi-line cell-values
        row = [self._split_cell_value(value) for value in row]

        # getting row height first (counting newlines in each cell value)
        row_height = 1
        # for value in row:
        #     row_height = max(row_height, len(value))    # len(value) is the number of lines in the cell-value
        row_height = max(len(lines) for lines in row)

        # building each text line for all values
        lines = []  # contains lines (to print) of table row
        for line_index in range(row_height):  # for each line
            line = []
            for column_index in range(len(row)):
                try:
                    value = row[column_index][line_index]
                except IndexError:
                    value = ""  # if no value for this line we just add an empty line
                line.append(
                    self._fill_h_cell_padding(value, self.column_widths[column_index])  # type: ignore
                )  # cell padding

            lines.append(
                "{}{}{}".format(  # noqa: UP032
                    self.cell_sep_char,  # first |
                    self.cell_sep_char.join(line),  # values separated by |
                    self.cell_sep_char,  # last |
                )
            )
        # joining all lines in row
        return self.newline.join(lines)


def draw_table(
    headers,
    table_data,
    row_sep_char=ROW_SEP_CHAR,
    headers_row_sep_char=HEADERS_ROW_SEP_CHAR,
    corner_char=CORNER_CHAR,
    cell_sep_char=CELL_SEP_CHAR,
    cell_fill_char=CELL_FILL_CHAR,
    min_h_padding=MIN_H_PADDING,
    column_keys=None,
    default_value=DEFAULT_VALUE,
    newline=NEWLINE,
):
    """
    Builds a string containing a printable table
    :param headers: A list of table headers
    :param table_data: A list of lists or list of dicts (see column keys)
    :param row_sep_char: The character that separates rows
    :param headers_row_sep_char: The character that separates headers row from the next row
    :param corner_char: The corner character (where row_sep_char and cell_sep_char intersect)
    :param cell_sep_char: The character which separates cells horizontally
    :param cell_fill_char: The character used for cell padding (usually a white space)
    :param min_h_padding: The minimum horizontal padding on each side of the cell value,
                          must be a positibe integer or 0
    :param column_keys: The keys of the table_data row dictionaries
                        (if not given table data is supposed to be a list of lists)
    :param default_value: Default value for missing fields in table_data,
                          makes sense only if table_data is a list of dicts
    :param newline: New line character(s) used in table data (for multi-line cell content),
                    the same will be used to construct the table
    :return: a string containing a printable table
    """
    return Table(
        headers,
        table_data,
        row_sep_char,
        headers_row_sep_char,
        corner_char,
        cell_sep_char,
        cell_fill_char,
        min_h_padding,
        column_keys,
        default_value,
        newline,
    ).draw()
