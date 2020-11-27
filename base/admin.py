from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from . import models

# Register your models here.


admin.site.register(models.Result)
admin.site.register(models.WeightMaximum)
admin.site.register(models.PeriodModel)
admin.site.register(models.Documentation, MarkdownxModelAdmin)


@admin.register(models.WeightModel)
class AdminWeightModel(admin.ModelAdmin):
    list_display = ["target", "start", "player", "state", "off"]


@admin.register(models.TargetVertex)
class AdminTargetVertex(admin.ModelAdmin):
    list_display = ["outline", "target", "player", "outline_time", "exact_off", "exact_noble"]


@admin.register(models.OutlineTime)
class AdminOutlineTime(admin.ModelAdmin):
    list_display = [
        "outline",
        "pk",
    ]


@admin.register(models.Overview)
class AdminOverview(admin.ModelAdmin):
    list_display = [
        "outline",
        "player",
        "token",
    ]


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


@admin.register(models.Tribe)
class AdminTribe(admin.ModelAdmin):
    list_display = [
        "tribe_id",
        "tag",
        "world",
    ]


@admin.register(models.Player)
class AdminPlayer(admin.ModelAdmin):
    list_display = [
        "player_id",
        "tribe_id",
        "name",
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
