from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from . import models

# Register your models here.


admin.site.register(models.Tribe)
admin.site.register(models.TargetVertex)
admin.site.register(models.WeightModel)
admin.site.register(models.Player)
admin.site.register(models.Result)
admin.site.register(models.Documentation, MarkdownxModelAdmin)


@admin.register(models.World)
class AdminWorld(admin.ModelAdmin):
    list_display = [
        "title",
        "world",
        "speed_world",
        "speed_units",
        "paladin",
        "archer",
        "militia",
    ]
    list_editable = [
        "world",
        "speed_world",
        "speed_units",
        "paladin",
        "archer",
        "militia",
    ]


@admin.register(models.VillageModel)
class AdminVillage(admin.ModelAdmin):
    list_display = [
        "village_id",
        "x_coord",
        "y_coord",
        "world",
    ]


@admin.register(models.Outline)
class AdminNewOutline(admin.ModelAdmin):
    list_display = [
        "name",
        "date",
        "world",
        "status",
        "owner",
        "ally_tribe_tag",
        "enemy_tribe_tag",
    ]
    list_editable = [
        "status",
        "owner",
    ]
