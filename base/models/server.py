# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.db import models
from timezone_field import TimeZoneField

from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class Server(models.Model):
    dns = models.CharField(max_length=50, primary_key=True)
    prefix = models.CharField(max_length=2)
    tz = TimeZoneField(use_pytz=False, default="Europe/Warsaw")

    objects = FetchErrorManager()

    def __str__(self):
        return self.dns

    class Meta:
        ordering = ("dns",)
