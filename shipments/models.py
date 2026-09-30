# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models.overview import Overview
from base.models.world import World
from tribal_wars_planer.fetch_error_manager import FetchErrorManager


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

    objects = FetchErrorManager()
