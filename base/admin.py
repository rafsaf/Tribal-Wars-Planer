from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Tribe)
admin.site.register(models.Player)
admin.site.register(models.Village)
admin.site.register(models.New_Outline)

@admin.register(models.World)
class AdminWorld(admin.ModelAdmin):
    list_display = [
        'title',
        'world',
        'speed_world',
        'speed_units',
    ]
    list_editable = [
        'world',
        'speed_world',
        'speed_units',
    ]
