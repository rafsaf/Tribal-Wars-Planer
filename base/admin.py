from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.World)
admin.site.register(models.Tribe)
admin.site.register(models.Player)
admin.site.register(models.Village)
admin.site.register(models.New_Outline)

