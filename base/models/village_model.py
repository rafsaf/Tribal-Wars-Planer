from django.db import models


class VillageModel(models.Model):
    """Village in the game"""

    village_id = models.IntegerField()
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    coord = models.CharField(max_length=7, db_index=True)
    player = models.ForeignKey(
        "Player", on_delete=models.CASCADE, null=True, blank=True
    )
    world = models.ForeignKey("World", on_delete=models.CASCADE)

    def __str__(self):
        return self.coord
