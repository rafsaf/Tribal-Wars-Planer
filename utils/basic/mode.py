# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from typing import Literal

from django.utils.translation import gettext as _


class Mode:
    VALID_MODE_TYPE: set[str] = {
        "menu",
        "time",
        "fake",
        "ruin",
        "add_and_remove",
    }

    def __init__(self, request_GET_mode: str | None):
        if request_GET_mode is None:
            self.mode = "menu"
        elif request_GET_mode in self.VALID_MODE_TYPE:
            self.mode = request_GET_mode
        else:
            self.mode = "menu"

    @property
    def is_menu(self):
        return self.mode == "menu"

    @property
    def is_time(self):
        return self.mode == "time"

    @property
    def is_fake(self):
        return self.mode == "fake"

    @property
    def is_ruin(self):
        return self.mode == "ruin"

    @property
    def is_add_and_remove(self):
        return self.mode == "add_and_remove"

    def trans_target(self) -> str:
        if self.is_menu:
            return _("Target")
        elif self.is_fake:
            return _("Fake Target")
        return _("Ruin Target")

    def trans_outline(self) -> str:
        if self.is_menu:
            return _("Outline")
        elif self.is_fake:
            return _("Fake Outline")
        return _("Ruin Outline")

    def __str__(self):
        return self.mode


class TargetMode:
    VALID_MODE_LIST: set[Literal["real", "fake", "ruin"]] = {
        "real",
        "fake",
        "ruin",
    }

    def __init__(self, request_GET_mode: str | None) -> None:
        if request_GET_mode is None:
            self.mode = "real"
        elif request_GET_mode in self.VALID_MODE_LIST:
            self.mode = request_GET_mode
        else:
            self.mode = "real"

    @property
    def is_real(self) -> bool:
        return self.mode == "real"

    @property
    def is_fake(self) -> bool:
        return self.mode == "fake"

    @property
    def is_ruin(self) -> bool:
        return self.mode == "ruin"

    @property
    def fake(self):
        if self.is_fake:
            return True
        return False

    @property
    def ruin(self):
        if self.is_ruin:
            return True
        return False
