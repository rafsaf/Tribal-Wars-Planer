# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from . import models

# Register your models here.

admin.site.register(models.PeriodModel)
admin.site.register(models.Result)
admin.site.register(models.Server)
admin.site.register(models.Message)

admin.site.register(models.Documentation, MarkdownxModelAdmin)


@admin.register(models.Payment)
class AdminPaymentModel(admin.ModelAdmin):
    list_display = [
        "user",
        "status",
        "from_stripe",
        "amount",
        "payment_date",
        "new_date",
    ]
    search_fields = ["user__username"]


@admin.register(models.Profile)
class AdminProfileModel(admin.ModelAdmin):
    list_display = ["user", "server", "validity_date"]
    search_fields = ["user__username"]


@admin.register(models.OutlineOverview)
class AdminOutlineOverview(admin.ModelAdmin):
    list_display = [
        "pk",
        "outline",
    ]
    search_fields = ["outline__owner__username", "outline__name"]


@admin.register(models.WeightMaximum)
class AdminWeightMaximumModel(admin.ModelAdmin):
    list_display = ["start", "outline", "player", "off_max", "nobleman_max"]
    search_fields = ["start"]
    readonly_fields = ["outline"]


@admin.register(models.WeightModel)
class AdminWeightModel(admin.ModelAdmin):
    list_display = ["target", "start", "player", "state", "off"]
    search_fields = ["start"]
    readonly_fields = ["target", "state"]


@admin.register(models.Stats)
class AdminStatsModel(admin.ModelAdmin):
    list_display = [
        "owner_name",
        "outline_pk",
        "created",
        "world",
        "premium_user",
        "overview_visited",
    ]
    search_fields = ["owner_name", "world", "outline_pk"]


@admin.register(models.TargetVertex)
class AdminTargetVertex(admin.ModelAdmin):
    list_display = [
        "outline",
        "target",
        "player",
        "outline_time",
        "exact_off",
        "exact_noble",
    ]
    search_fields = ["target"]
    readonly_fields = ["outline"]


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
        "created",
        "player",
        "token",
    ]
    search_fields = ["player", "outline__ally_tribe_tag", "outline__name"]


@admin.register(models.World)
class AdminWorld(admin.ModelAdmin):
    list_display = [
        "server",
        "postfix",
        "connection_errors",
        "speed_world",
        "speed_units",
        "paladin",
        "archer",
        "militia",
        "max_noble_distance",
    ]
    list_editable = [
        "connection_errors",
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
        "coord",
        "world",
        "player",
    ]
    search_fields = ["coord", "world__postfix", "village_id"]
    readonly_fields = ["player"]


@admin.register(models.Tribe)
class AdminTribe(admin.ModelAdmin):
    list_display = [
        "tribe_id",
        "tag",
        "world",
    ]
    search_fields = ["tag", "world__postfix"]


@admin.register(models.Player)
class AdminPlayer(admin.ModelAdmin):
    list_display = [
        "player_id",
        "name",
        "world",
        "tribe",
    ]
    search_fields = ["name", "world__postfix"]


@admin.register(models.Outline)
class AdminNewOutline(admin.ModelAdmin):
    list_display = [
        "name",
        "owner",
        "created",
        "world",
        "ally_tribe_tag",
        "enemy_tribe_tag",
    ]
    search_fields = ["owner__username", "world__postfix"]
