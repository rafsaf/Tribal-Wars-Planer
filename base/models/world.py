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


from django.db import models
from django.utils.translation import gettext_lazy

from base.models.server import Server


class World(models.Model):
    """World in the game"""

    STATUS_CHOICES: list[tuple[str, str]] = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    postfix = models.CharField(max_length=10)
    connection_errors = models.IntegerField(default=0)
    speed_world = models.FloatField(default=1)
    speed_units = models.FloatField(default=1)
    paladin = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    archer = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    militia = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    max_noble_distance = models.IntegerField(default=500)
    morale = models.IntegerField(default=1)
    casual_attack_block_ratio = models.IntegerField(null=True, default=None, blank=True)
    pending_delete = models.BooleanField(default=False)
    fanout_key_text_player = models.CharField(default="__0", max_length=200)
    fanout_key_text_tribe = models.CharField(default="__0", max_length=200)
    fanout_key_text_village = models.CharField(default="__0", max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.server.prefix + self.postfix

    def last_modified_timestamp(self) -> float:
        world, data_type, timestampt_str = self.fanout_key_text_village.split("_")
        return float(timestampt_str)

    def human(self, prefix: bool = False):
        if prefix:
            server_prefix: str = self.server.prefix
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
