from django.db import models


class OutlineTime(models.Model):
    """Handle Time for Target"""

    outline = models.ForeignKey("Outline", on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
