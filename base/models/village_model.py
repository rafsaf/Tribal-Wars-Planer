# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import typing

from django.db import models

from base.models.player import Player
from base.models.world import World
from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class VillageModel(models.Model):
    """Village in the game"""

    village_id = models.IntegerField()
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    coord = models.CharField(max_length=7)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FetchErrorManager()

    if typing.TYPE_CHECKING:
        player_id: int | None
        world_id: int

    class Meta:
        indexes = [
            models.Index(fields=["world", "coord"]),
            models.Index(fields=["world", "player"]),
            models.Index(fields=["world", "village_id"]),
        ]

    def __str__(self):
        return self.coord
