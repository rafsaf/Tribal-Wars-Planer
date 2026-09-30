# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.db import models

from base.models.outline import Outline
from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class Result(models.Model):
    """Presents Outline and Deff results"""

    outline = models.OneToOneField(Outline, on_delete=models.CASCADE, primary_key=True)
    results_get_deff = models.TextField(default="")
    results_outline = models.TextField(default="")
    results_players = models.TextField(default="")
    results_sum_up = models.TextField(default="")
    results_export = models.TextField(default="")

    objects = FetchErrorManager()

    def __str__(self):
        return self.outline.name + " results"
