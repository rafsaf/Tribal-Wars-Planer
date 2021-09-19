from django.db import models


class Result(models.Model):
    """Presents Outline and Deff results"""

    outline = models.OneToOneField(
        "Outline", on_delete=models.CASCADE, primary_key=True
    )
    results_get_deff = models.TextField(default="")
    results_outline = models.TextField(default="")
    results_players = models.TextField(default="")
    results_sum_up = models.TextField(default="")
    results_export = models.TextField(default="")

    def __str__(self):
        return self.outline.name + " results"
