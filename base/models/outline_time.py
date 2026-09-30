# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.db import models

from base.models.outline import Outline
from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class OutlineTime(models.Model):
    """Handle Time for Target"""

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    objects = FetchErrorManager()
