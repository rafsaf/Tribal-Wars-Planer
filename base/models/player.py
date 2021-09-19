from django.db import models


class Player(models.Model):
    """Player in the game"""

    player_id = models.IntegerField()
    name = models.TextField(db_index=True)
    tribe = models.ForeignKey("Tribe", on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey("World", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
