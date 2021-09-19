from typing import TYPE_CHECKING, Union

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

    def tw_stats_link_to_village(self, village_id: Union[str, int]):
        return (
            f"https://{self.server.prefix}.twstats.com/{str(self)}/index.php?"
            f"page=village&id={village_id}"
        )
