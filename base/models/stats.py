from django.db import models


class Stats(models.Model):
    outline = models.ForeignKey(
        "Outline", on_delete=models.SET_NULL, null=True, blank=True
    )
    outline_pk = models.IntegerField()
    owner_name = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    world = models.CharField(max_length=50)
    premium_user = models.BooleanField()
    off_troops = models.IntegerField(default=0)
    deff_troops = models.IntegerField(default=0)
    real_targets = models.IntegerField(default=0)
    fake_targets = models.IntegerField(default=0)
    ruin_targets = models.IntegerField(default=0)
    troops_refreshed = models.IntegerField(default=0)
    outline_written = models.IntegerField(default=0)
    available_troops = models.IntegerField(default=0)
    date_change = models.IntegerField(default=0)
    settings_change = models.IntegerField(default=0)
    night_change = models.IntegerField(default=0)
    ruin_change = models.IntegerField(default=0)
    building_order_change = models.IntegerField(default=0)
    time_created = models.IntegerField(default=0)
    go_back_clicked = models.IntegerField(default=0)
    finish_outline_clicked = models.IntegerField(default=0)
    overview_visited = models.IntegerField(default=0)
