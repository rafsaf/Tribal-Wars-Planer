# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import typing

from django.db import models

from base.models.tribe import Tribe
from base.models.world import World
from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class Player(models.Model):
    """Player in the game"""

    player_id = models.IntegerField()
    name = models.TextField()
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, db_index=True)
    villages = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FetchErrorManager()

    if typing.TYPE_CHECKING:
        tribe_id: int | None
        world_id: int

    def __str__(self):
        return self.name
