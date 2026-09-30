# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.db import models

from base.models.world import World
from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class Tribe(models.Model):
    """Tribe in game"""

    tribe_id = models.IntegerField()
    tag = models.TextField(db_index=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FetchErrorManager()

    def __str__(self):
        return self.tag
