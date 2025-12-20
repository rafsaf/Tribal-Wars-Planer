# Copyright 2025 Rafał Safin (rafsaf). All Rights Reserved.
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

import enum

from django.utils.translation import gettext_lazy


class SEND_TEXT(enum.StrEnum):
    FAKE_NOBLE = "Send FAKE NOBLE"
    FAKE = "Send FAKE"
    RUIN = "Send RUIN"
    NOBLE = "Send NOBLE"
    OFF = "Send OFF"


SEND_TEXT_TRANSLATION = {
    SEND_TEXT.FAKE_NOBLE.value: gettext_lazy("Send FAKE NOBLE"),
    SEND_TEXT.FAKE.value: gettext_lazy("Send FAKE"),
    SEND_TEXT.RUIN.value: gettext_lazy("Send RUIN"),
    SEND_TEXT.NOBLE.value: gettext_lazy("Send NOBLE"),
    SEND_TEXT.OFF.value: gettext_lazy("Send OFF"),
}
