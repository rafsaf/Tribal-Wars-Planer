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
from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from base.models.world import World

from . import models

# Register your models here.


admin.site.register(models.PeriodModel)
admin.site.register(models.Server)
admin.site.register(models.Message)
admin.site.register(models.PDFPaymentSummary)


@admin.register(models.StripePrice)
class AdminStripePriceModel(admin.ModelAdmin):
    list_display = [
        "amount",
        "currency",
        "active",
        "price_id",
    ]


@admin.register(models.StripeProduct)
class AdminStripeProductModel(admin.ModelAdmin):
    list_display = [
        "name",
        "months",
        "active",
        "product_id",
    ]


@admin.register(models.Result)
class AdminResult(admin.ModelAdmin):
    readonly_fields = ["outline"]


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
    readonly_fields = ["outline", "targets_json", "weights_json"]


@admin.register(models.WeightMaximum)
class AdminWeightMaximumModel(admin.ModelAdmin):
    list_display = [
        "start",
        "outline",
        "player",
        "off_max",
        "off_left",
        "nobleman_max",
        "nobleman_left",
        "catapult_max",
        "catapult_left",
    ]
    search_fields = ["start", "outline__name"]
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
    readonly_fields = ["outline"]


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
    readonly_fields = ["outline", "outline_time"]


@admin.register(models.OutlineTime)
class AdminOutlineTime(admin.ModelAdmin):
    list_display = [
        "outline",
        "pk",
    ]
    readonly_fields = ["outline"]


@admin.register(models.Overview)
class AdminOverview(admin.ModelAdmin):
    list_display = [
        "outline",
        "player",
        "created",
    ]
    search_fields = ["player", "outline__ally_tribe_tag", "outline__name"]
    readonly_fields = ["outline_overview", "outline"]


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
    search_fields = ["postfix", "server__dns"]
    list_editable = [
        "connection_errors",
        "speed_world",
        "speed_units",
        "paladin",
        "archer",
        "militia",
    ]

    def get_deleted_objects(
        self, objs: QuerySet[World], request: HttpRequest
    ) -> tuple[list[Any], dict[Any, Any], set[Any], list[Any]]:
        worlds_list = [world.human(prefix=True) for world in objs]
        model_count = {
            models.World._meta.verbose_name_plural: f"{len(objs)} ({', '.join(worlds_list)})",
            models.VillageModel._meta.verbose_name_plural: models.VillageModel.objects.filter(
                world__in=objs
            ).count(),
            models.Player._meta.verbose_name_plural: models.Player.objects.filter(
                world__in=objs
            ).count(),
            models.Tribe._meta.verbose_name_plural: models.Tribe.objects.filter(
                world__in=objs
            ).count(),
            models.Outline._meta.verbose_name_plural: models.Outline.objects.filter(
                world__in=objs
            ).count(),
            models.OutlineOverview._meta.verbose_name_plural: models.OutlineOverview.objects.filter(
                outline__world__in=objs
            ).count(),
            models.Overview._meta.verbose_name_plural: models.Overview.objects.filter(
                outline_overview__outline__world__in=objs
            ).count(),
            models.WeightMaximum._meta.verbose_name_plural: models.WeightMaximum.objects.filter(
                outline__world__in=objs
            ).count(),
            models.WeightModel._meta.verbose_name_plural: models.WeightModel.objects.filter(
                state__outline__world__in=objs
            ).count(),
            models.TargetVertex._meta.verbose_name_plural: models.TargetVertex.objects.filter(
                outline__world__in=objs
            ).count(),
            models.OutlineTime._meta.verbose_name_plural: models.OutlineTime.objects.filter(
                outline__world__in=objs
            ).count(),
            models.Result._meta.verbose_name_plural: models.Result.objects.filter(
                outline__world__in=objs
            ).count(),
        }
        return (
            [],
            model_count,
            set(),
            [],
        )


@admin.register(models.VillageModel)
class AdminVillage(admin.ModelAdmin):
    list_display = [
        "village_id",
        "coord",
        "world",
        "player",
    ]
    search_fields = ["coord", "world__postfix", "village_id"]
    readonly_fields = ["player", "world"]


@admin.register(models.Tribe)
class AdminTribe(admin.ModelAdmin):
    list_display = [
        "tribe_id",
        "tag",
        "world",
    ]
    search_fields = ["tag", "world__postfix"]
    readonly_fields = ["world"]


@admin.register(models.Player)
class AdminPlayer(admin.ModelAdmin):
    list_display = [
        "player_id",
        "name",
        "world",
        "tribe",
        "created_at",
        "updated_at",
    ]
    search_fields = ["name", "world__postfix"]
    readonly_fields = ["world", "tribe"]


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
