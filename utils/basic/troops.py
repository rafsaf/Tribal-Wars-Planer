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

import json
from typing import Literal

from django.forms.utils import ErrorDict

from base.models import Outline


class Troops:
    def __init__(
        self, outline: Outline, name: Literal["off_troops", "deff_troops"]
    ) -> None:
        self.troops: str = outline.__getattribute__(name)
        self.name = name
        self.errors: list[dict[str, str]] | None = None
        self.empty: bool = False
        self.get_json = ""

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
            self.get_json = json.dumps(self.errors)
