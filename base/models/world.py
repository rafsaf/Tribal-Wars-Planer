# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
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

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy

if TYPE_CHECKING:
    from base.models import Server


class World(models.Model):
    """World in the game"""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    server = models.ForeignKey("Server", on_delete=models.CASCADE)
    postfix = models.CharField(max_length=10)
    last_update = models.DateTimeField(auto_now_add=True)

    connection_errors = models.IntegerField(default=0)
    speed_world = models.FloatField(null=True, blank=True, default=1)
    speed_units = models.FloatField(null=True, blank=True, default=1)
    paladin = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    archer = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    militia = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    max_noble_distance = models.IntegerField(default=50)
    morale = models.IntegerField(default=1)
    etag_player = models.CharField(max_length=200, default="")
    etag_tribe = models.CharField(max_length=200, default="")
    etag_village = models.CharField(max_length=200, default="")

    def __str__(self):
        server: "Server" = self.server
        return server.prefix + self.postfix

    def human(self, prefix: bool = False):
        server: "Server" = self.server
        if prefix:
            server_prefix: str = server.prefix
            last = " " + server_prefix.upper()
        else:
            last = ""
        return gettext_lazy("World ") + self.postfix + last

    def link_to_game(self, addition: str = ""):
        return f"https://{str(self)}." f"{self.server.dns}" f"{addition}"

    def tw_stats_link_to_village(self, village_id: str | int):
        return (
            f"https://{self.server.prefix}.twstats.com/{str(self)}/index.php?"
            f"page=village&id={village_id}"
        )
