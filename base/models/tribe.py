from django.db import models


class Tribe(models.Model):
    """Tribe in game"""

    tribe_id = models.IntegerField()
    tag = models.TextField(db_index=True)
    world = models.ForeignKey("World", on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.tag
