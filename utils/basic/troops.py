import json
from typing import Dict, List, Literal, Optional

from django.forms.utils import ErrorDict

from base.models import Outline


class Troops:
    def __init__(
        self, outline: Outline, name: Literal["off_troops", "deff_troops"]
    ) -> None:
        self.troops: str = outline.__getattribute__(name)
        self.name = name
        self.errors: Optional[List[Dict[str, str]]] = None
        self.empty: bool = False
        self.get_json = ""

    def set_troops(self, troops: Optional[str]):
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
