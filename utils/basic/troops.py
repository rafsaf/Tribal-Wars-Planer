# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import json
from typing import Literal

from django.forms.utils import ErrorDict
from django.utils.translation import gettext

from base.models import Outline


class Troops:
    def __init__(
        self, outline: Outline, name: Literal["off_troops", "deff_troops"]
    ) -> None:
        self.troops: str = outline.__getattribute__(name)
        self.name = name
        self.errors: list[dict[str, str]] | None = None
        self.non_field_errors: list[dict[str, str]] | None = None
        self.empty: bool = False
        self.get_json = ""
        self.first_error_msg = ""
        self.second_error_msg = ""

    def set_troops(self, troops: str | None):
        if troops is None:
            self.troops = ""
        else:
            self.troops = troops

    def set_errors(self, error_dict: ErrorDict):
        if len(self.troops) == 0:
            self.empty = True
        else:
            self.errors = json.loads(error_dict.as_json())[self.name]
            self.non_field_errors = json.loads(error_dict.as_json()).get("__all__", [])
            self.get_json = json.dumps(self.errors)

    def set_first_error_msg(self, message: str):
        if self.errors and len(self.errors):
            line_number = int(self.errors[0]["message"])
            self.first_error_msg = gettext("Line %s: ") % f"{line_number + 1}" + message

    def set_second_error_msg(self, message: str):
        self.second_error_msg = message
