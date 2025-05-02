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
