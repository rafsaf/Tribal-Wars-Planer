# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.db import models

from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class Message(models.Model):
    date = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=20, default="bug fix")
    text = models.TextField(default="")

    objects = FetchErrorManager()
