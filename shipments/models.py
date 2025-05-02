# Create your models here.
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models.overview import Overview
from base.models.world import World


class Shipment(models.Model):
    name = models.CharField(max_length=24)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    overviews = models.ManyToManyField(Overview, blank=True)
    sent_lst = ArrayField(models.BigIntegerField(), blank=True, default=list)
    hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
