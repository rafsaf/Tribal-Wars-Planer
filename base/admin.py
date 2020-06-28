from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from . import models

# Register your models here.


admin.site.register(models.Tribe)
admin.site.register(models.Player)
admin.site.register(models.Results)
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


@admin.register(models.Village)
class AdminVillage(admin.ModelAdmin):
    list_display = [
        "village_id",
        "x",
        "y",
        "world",
    ]


@admin.register(models.New_Outline)
class AdminNewOutline(admin.ModelAdmin):
    list_display = [
        "nazwa",
        "data_akcji",
        "swiat",
        "status",
        "owner",
        "moje_plemie_skrot",
        "przeciwne_plemie_skrot",
    ]
    list_editable = [
        "status",
        "owner",
    ]
