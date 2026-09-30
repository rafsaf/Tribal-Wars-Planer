# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import datetime
import typing

from django.db import models
from django.utils.translation import gettext_lazy

from base.models.outline_time import OutlineTime
from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class PeriodModel(models.Model):
    """Handle one period of time in outline specification"""

    STATUS = [
        ("all", gettext_lazy("All (left)")),
        ("random", gettext_lazy("Random")),
        ("exact", gettext_lazy("Exact")),
    ]
    UNITS = [
        ("noble", gettext_lazy("Noble")),
        ("ram", gettext_lazy("Ram")),
    ]
    outline_time = models.ForeignKey(OutlineTime, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS)
    unit = models.CharField(max_length=15, choices=UNITS)
    from_number = models.IntegerField(null=True, default=None, blank=True)
    to_number = models.IntegerField(null=True, default=None, blank=True)
    from_time = models.TimeField(default=datetime.time(hour=7))
    to_time = models.TimeField(default=datetime.time(hour=7))

    if typing.TYPE_CHECKING:
        outline_time_id: int

    objects = FetchErrorManager()
