from django.db import models


class OutlineOverview(models.Model):
    outline = models.ForeignKey(
        "Outline", on_delete=models.SET_NULL, null=True, blank=True
    )
    weights_json = models.TextField(default="", blank=True)
    targets_json = models.TextField(default="", blank=True)
