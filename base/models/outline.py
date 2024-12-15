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

import datetime
import typing
from hashlib import sha256

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.paginator import Paginator
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models, transaction
from django.db.models import Count, F, Q, Sum
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy

from base.models.world import World
from utils.buildings import BUILDING, BUILDINGS_TRANSLATION


def building_default_list() -> list[str]:
    return [
        BUILDING.FARM.value,
        BUILDING.HEADQUARTERS.value,
        BUILDING.SMITHY.value,
    ]


class Outline(models.Model):
    """Outline with all informations about it"""

    VALID_SORT_CHOICES: list[tuple[str, str]] = [
        ("distance", "distance"),
        ("random_distance", "random_distance"),
        ("-distance", "-distance"),
        ("-off_left", "-off_left"),
        ("-nobleman_left", "-nobleman_left"),
        ("closest_offs", "closest_offs"),
        ("random_offs", "random_offs"),
        ("farthest_offs", "farthest_offs"),
        ("closest_noblemans", "closest_noblemans"),
        ("random_noblemans", "random_noblemans"),
        ("farthest_noblemans", "farthest_noblemans"),
        ("closest_noble_offs", "closest_noble_offs"),
        ("random_noble_offs", "random_noble_offs"),
        ("farthest_noble_offs", "farthest_noble_offs"),
    ]

    STATUS_CHOICES: list[tuple[str, str]] = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    MODE_OFF: list[tuple[str, str]] = [
        ("closest", gettext_lazy("Closest Front")),
        ("close", gettext_lazy("Close Back")),
        ("random", gettext_lazy("Random Back")),
        ("far", gettext_lazy("Far Back")),
    ]

    MODE_NOBLE: list[tuple[str, str]] = [
        ("closest", gettext_lazy("Closest Front")),
        ("close", gettext_lazy("Close Back")),
        ("random", gettext_lazy("Random Back")),
        ("far", gettext_lazy("Far Back")),
    ]

    MODE_DIVISION: list[tuple[str, str]] = [
        ("divide", gettext_lazy("Divide off with nobles")),
        ("not_divide", gettext_lazy("Dont't divide off")),
        ("separatly", gettext_lazy("Off and nobles separatly")),
    ]

    MODE_SPLIT: list[tuple[str, str]] = [
        ("together", gettext_lazy("Nobles from one village as one command")),
        ("split", gettext_lazy("Nobles from one village as many commands")),
    ]

    NOBLE_GUIDELINES: list[tuple[str, str]] = [
        ("one", gettext_lazy("Try send all nobles to one target")),
        ("many", gettext_lazy("Nobles to one or many targets")),
        ("single", gettext_lazy("Try single nobles from many villages")),
    ]

    HIDE_CHOICES: list[tuple[str, str]] = [
        ("all", gettext_lazy("All")),
        ("front", gettext_lazy("Front")),
        ("back", gettext_lazy("Back (Rear)")),
        ("away", gettext_lazy("Away")),
        ("hidden", gettext_lazy("Hidden")),
    ]

    BUILDINGS = BUILDINGS_TRANSLATION.items()

    RUINED_VILLAGES_POINTS: list[tuple[str, str]] = [
        ("big", gettext_lazy("Average greater than 8k")),
        ("medium", gettext_lazy("Average 5-8k")),
    ]

    CATAPULTS_NUMBER: list[tuple[int, str]] = [
        (25, "25"),
        (50, "50"),
        (75, "75"),
        (100, "100"),
        (150, "150"),
        (200, "200"),
    ]

    FAKE_MIN_OFF_CHOICES: list[tuple[str, str]] = [
        ("off", gettext_lazy("Fakes only from off villages")),
        ("all", gettext_lazy("Fakes from all villages")),
    ]

    SENDING_OPTIONS: list[tuple[str, str]] = [
        (
            "default",
            gettext_lazy("(Default) Auto generated, fully equipped safe links"),
        ),
        ("string", gettext_lazy("Text simple directly in message")),
        ("new_extended", gettext_lazy("New text extended directly in message")),
        ("extended", gettext_lazy("Old text extended directly in message")),
        ("deputy", gettext_lazy("Text for deputy directly in message")),
    ]

    ARMY_COLLECTION = "Army collection"
    DEFF_COLLECTION = "Deff collection"
    INPUT_DATA_TYPES: list[tuple[str, str]] = [
        (ARMY_COLLECTION, gettext_lazy("Army collection")),
        (DEFF_COLLECTION, gettext_lazy("Deff collection ")),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=24)
    parent_outline = models.ForeignKey(
        "Outline", on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    written = models.CharField(choices=STATUS_CHOICES, max_length=8, default="inactive")
    editable = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    ally_tribe_tag = ArrayField(models.CharField(max_length=6), default=list)
    enemy_tribe_tag = ArrayField(models.CharField(max_length=6), default=list)

    choice_sort = models.CharField(
        max_length=50, choices=VALID_SORT_CHOICES, default="distance"
    )
    initial_outline_targets = models.TextField(blank=True, default="")
    initial_outline_fakes = models.TextField(blank=True, default="")
    initial_outline_ruins = models.TextField(blank=True, default="")

    initial_outline_catapult_max_value = models.IntegerField(
        default=200, choices=CATAPULTS_NUMBER
    )
    initial_outline_catapult_min_value = models.IntegerField(
        default=25, choices=CATAPULTS_NUMBER
    )
    initial_outline_off_left_catapult = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(400)]
    )
    initial_outline_average_ruining_points = models.CharField(
        max_length=150, choices=RUINED_VILLAGES_POINTS, default="big"
    )
    initial_outline_buildings = ArrayField(
        models.CharField(max_length=100, choices=BUILDINGS),
        default=building_default_list,
    )
    initial_outline_min_off = models.IntegerField(
        default=19000,
        validators=[MinValueValidator(1), MaxValueValidator(28000)],
    )
    initial_outline_max_off = models.IntegerField(
        default=28000,
        validators=[MinValueValidator(1), MaxValueValidator(28000)],
    )
    initial_outline_front_dist = models.IntegerField(
        default=10, validators=[MinValueValidator(0), MaxValueValidator(500)]
    )
    initial_outline_maximum_off_dist = models.IntegerField(
        default=100, validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    initial_outline_target_dist = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(10000)]
    )
    initial_outline_excluded_coords = models.TextField(default="", blank=True)
    initial_outline_fake_limit = models.IntegerField(
        default=4, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    initial_outline_fake_mode = models.CharField(
        max_length=60, choices=FAKE_MIN_OFF_CHOICES, default="off"
    )
    initial_outline_minimum_noble_troops = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(28000)],
    )
    initial_outline_nobles_limit = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(250)],
    )

    input_data_type = models.CharField(
        max_length=32, default="Army collection", choices=INPUT_DATA_TYPES
    )
    off_troops = models.TextField(
        blank=True,
        default="",
    )
    off_troops_hash = models.CharField(max_length=64, default="", blank=True)
    off_troops_weightmodels_hash = models.CharField(
        max_length=64, default="", blank=True
    )
    deff_troops = models.TextField(
        blank=True,
        default="",
    )
    deff_troops_hash = models.CharField(max_length=64, default="", blank=True)
    deff_troops_weightmodels_hash = models.CharField(
        max_length=64, default="", blank=True
    )

    avaiable_offs = ArrayField(models.IntegerField(), default=list, blank=True)
    avaiable_nobles = ArrayField(models.IntegerField(), default=list, blank=True)
    avaiable_offs_near = ArrayField(models.IntegerField(), default=list, blank=True)
    avaiable_nobles_near = ArrayField(models.IntegerField(), default=list, blank=True)
    available_catapults = ArrayField(
        models.IntegerField(), default=list, blank=True, max_length=4
    )
    avaiable_ruins = models.IntegerField(default=None, null=True, blank=True)

    mode_off = models.CharField(max_length=15, choices=MODE_OFF, default="random")
    mode_noble = models.CharField(max_length=15, choices=MODE_NOBLE, default="closest")
    mode_division = models.CharField(
        max_length=15, choices=MODE_DIVISION, default="not_divide"
    )
    mode_guide = models.CharField(
        max_length=15, choices=NOBLE_GUIDELINES, default="one"
    )
    mode_split = models.CharField(max_length=15, choices=MODE_SPLIT, default="split")

    filter_weights_min = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(30000)]
    )
    filter_weights_catapults_min = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(3000)]
    )
    filter_weights_nobles_min = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    filter_weights_max = models.IntegerField(
        default=30000,
        validators=[MinValueValidator(0), MaxValueValidator(30000)],
    )
    filter_card_number = models.IntegerField(
        default=12,
        validators=[MinValueValidator(1), MaxValueValidator(40)],
    )
    filter_hide_front = models.CharField(
        max_length=20, choices=HIDE_CHOICES, default="all"
    )
    morale_on_targets_greater_than = models.IntegerField(
        default=100, validators=[MinValueValidator(25), MaxValueValidator(100)]
    )
    morale_on = models.BooleanField(default=False)
    filter_targets_number = models.IntegerField(
        default=25,
        validators=[MinValueValidator(1), MaxValueValidator(200)],
    )
    simple_textures = models.BooleanField(default=False)
    default_show_hidden = models.BooleanField(default=False)
    sending_option = models.CharField(
        default="default", choices=SENDING_OPTIONS, max_length=50
    )
    title_message = models.CharField(
        max_length=200, default=gettext_lazy("Outline Targets")
    )
    send_message_with_url = models.BooleanField(default=True)
    text_message = models.CharField(max_length=2000, default="", blank=True)
    night_bonus = models.BooleanField(default=False)
    enter_t1 = models.IntegerField(default=7)
    enter_t2 = models.IntegerField(default=12)
    default_off_time_id = models.IntegerField(default=None, null=True, blank=True)
    default_fake_time_id = models.IntegerField(default=None, null=True, blank=True)
    default_ruin_time_id = models.IntegerField(default=None, null=True, blank=True)

    deff_collection_text_in_village = models.CharField(
        max_length=256, default="", blank=True
    )
    deff_collection_text_enroute = models.CharField(
        max_length=256, default="", blank=True
    )

    if typing.TYPE_CHECKING:
        parent_outline_id: int

    class Meta:
        ordering = ("-created",)

    def get_input_data_trans(self):
        if self.input_data_type == self.ARMY_COLLECTION:
            return gettext_lazy("Army collection")
        else:
            return gettext_lazy("Deff collection ")

    def __str__(self):
        name_text = gettext_lazy("Name")
        return f"ID: {self.pk}, {name_text}: {self.name}"

    def get_or_set_off_troops_hash(self, force_recalculate: bool = False):
        if force_recalculate or not self.off_troops_hash:
            new_hash = sha256(
                self.off_troops.encode(), usedforsecurity=False
            ).hexdigest()
            self.off_troops_hash = new_hash
            self.save(update_fields=["off_troops_hash"])
            return new_hash
        return self.off_troops_hash

    def get_or_set_deff_troops_hash(self, force_recalculate: bool = False):
        if force_recalculate or not self.deff_troops_hash:
            new_hash = sha256(
                self.deff_troops.encode(), usedforsecurity=False
            ).hexdigest()
            self.deff_troops_hash = new_hash
            self.save(update_fields=["deff_troops_hash"])
            return new_hash
        return self.deff_troops_hash

    @transaction.atomic
    def remove_user_outline(self):
        from base import forms
        from base.models import (
            Overview,
            Result,
            TargetVertex,
            WeightMaximum,
            WeightModel,
        )
        from utils.basic import TargetMode

        self.written = "inactive"
        self.avaiable_offs = []
        self.avaiable_offs_near = []
        self.avaiable_nobles = []
        self.avaiable_nobles_near = []
        self.available_catapults = []
        self.avaiable_ruins = None
        self.filter_weights_min = 0
        self.filter_weights_catapults_min = 0
        self.filter_weights_nobles_min = 0
        self.filter_weights_max = 30000
        self.filter_hide_front = "all"
        self.choice_sort = "distance"
        self.default_off_time_id = None
        self.default_fake_time_id = None
        self.default_ruin_time_id = None

        WeightModel.objects.filter(target__outline=self).delete()

        WeightMaximum.objects.filter(outline=self).update(
            off_left=F("off_max"),
            off_state=0,
            nobleman_left=F("nobleman_max"),
            nobleman_state=0,
            catapult_left=F("catapult_max"),
            catapult_state=0,
            hidden=False,
            first_line=False,
            too_far_away=False,
            fake_limit=self.initial_outline_fake_limit,
            nobles_limit=self.initial_outline_nobles_limit,
        )
        form1 = forms.InitialOutlineForm(
            {"target": self.initial_outline_targets},
            outline=self,
            target_mode=TargetMode("real"),
        )
        form2 = forms.InitialOutlineForm(
            {"target": self.initial_outline_fakes},
            outline=self,
            target_mode=TargetMode("fake"),
        )
        form3 = forms.InitialOutlineForm(
            {"target": self.initial_outline_ruins},
            outline=self,
            target_mode=TargetMode("ruin"),
        )
        if not form1.is_valid() or not form2.is_valid() or not form3.is_valid():
            TargetVertex.objects.filter(outline=self).delete()

        Overview.objects.filter(outline=self, removed=False).update(removed=True)
        result: Result = Result.objects.get(outline=self)
        result.results_outline = ""
        result.results_players = ""
        result.results_sum_up = ""
        result.results_export = ""
        result.save(
            update_fields=[
                "results_outline",
                "results_players",
                "results_sum_up",
                "results_export",
            ]
        )
        self.save(
            update_fields=[
                "written",
                "avaiable_offs",
                "avaiable_offs_near",
                "avaiable_nobles",
                "avaiable_nobles_near",
                "available_catapults",
                "avaiable_ruins",
                "filter_weights_min",
                "filter_weights_catapults_min",
                "filter_weights_nobles_min",
                "filter_weights_max",
                "filter_hide_front",
                "choice_sort",
                "default_off_time_id",
                "default_fake_time_id",
                "default_ruin_time_id",
            ]
        )

    def expires_in(self) -> str:
        base: str = gettext_lazy("Expires ")
        postfix: str = "</small>"

        minus_35_days = timezone.now() - datetime.timedelta(days=35)
        expire: datetime.timedelta = self.created - minus_35_days

        if expire.days > 7:
            prefix = "<small class='md-correct2'>"
        else:
            prefix = "<small class='md-error'>"

        return (
            prefix
            + base
            + gettext_lazy("in")
            + f" {expire.days} "
            + gettext_lazy("days")
            + postfix
        )

    @cached_property
    def get_all_targets(self):
        from base.models import TargetVertex

        return list(TargetVertex.objects.filter(outline=self))

    def count_targets(self) -> int:
        return len(
            [
                target
                for target in self.get_all_targets
                if not target.fake and not target.ruin
            ]
        )

    def count_fake(self) -> int:
        return len(
            [
                target
                for target in self.get_all_targets
                if target.fake and not target.ruin
            ]
        )

    def count_ruin(self) -> int:
        return len(
            [
                target
                for target in self.get_all_targets
                if not target.fake and target.ruin
            ]
        )

    def count_off(self) -> int:
        from base.models import WeightMaximum

        return (
            WeightMaximum.objects.filter(outline=self)
            .filter(
                off_left__gte=self.initial_outline_min_off,
                off_left__lte=self.initial_outline_max_off,
            )
            .count()
        )

    def count_noble(self) -> int:
        from base.models import WeightMaximum

        return (
            WeightMaximum.objects.filter(outline=self).aggregate(
                nobles=Sum("nobleman_left")
            )["nobles"]
            or 0
        )

    def count_catapults(self) -> int:
        from utils.avaiable_troops import get_available_ruins

        return get_available_ruins(self)

    def pagin_targets(  # noqa: PLR0912
        self,
        page: str | None,
        fake: bool = False,
        ruin: bool = False,
        every: bool = False,
        filtr: str = "",
        not_empty_only: bool = False,
        related: bool = False,
    ):
        from base.models import TargetVertex

        all_targets: QuerySet[TargetVertex] = TargetVertex.objects.filter(
            outline=self
        ).order_by("pk")

        if not every:
            targets = all_targets.filter(fake=fake, ruin=ruin)
        else:
            targets = all_targets

        if not_empty_only:
            targets = targets.annotate(num_of_weights=Count("weightmodel")).filter(
                num_of_weights__gt=0
            )

        if related:
            targets = targets.select_related("outline_time")

        if filtr != "":
            if "|" in filtr:
                targets = targets.filter(target__icontains=filtr)
            elif filtr.isnumeric() and len(filtr) <= 3:
                targets = targets.filter(
                    Q(target__icontains=filtr) | Q(player__icontains=filtr)
                )
            elif (
                filtr.startswith("command")
                and filtr[7] in [">", "<", "="]
                and filtr[8:].isnumeric()
            ):
                if not not_empty_only:
                    targets = targets.annotate(num_of_weights=Count("weightmodel"))
                if filtr[7] == ">":
                    targets = targets.filter(num_of_weights__gt=int(filtr[8:]))
                elif filtr[7] == "=":
                    targets = targets.filter(num_of_weights=int(filtr[8:]))
                else:
                    targets = targets.filter(num_of_weights__lt=int(filtr[8:]))

            else:
                targets = targets.filter(player__icontains=filtr)

        pagin = Paginator(targets, self.filter_targets_number)
        return pagin.get_page(page)

    def targets_query(self, target_lst):
        from base.models import TargetVertex, WeightModel

        result: dict[TargetVertex, list[WeightModel]] = {}
        for target in target_lst:
            result[target] = list()
        weights: QuerySet[WeightModel] = (
            WeightModel.objects.select_related("target")
            .filter(target__in=target_lst)
            .order_by("order")
        )
        for weight in weights:
            weight.distance = round(weight.distance_to_village(weight.target.target), 1)
            weight.off = f"{round(weight.off / 1000, 1)}k"  # type: ignore
            result[weight.target].append(weight)
        return result.items()

    def create_target(self, target_type: str | None, coord: str | None) -> None:
        from base.models import TargetVertex, VillageModel

        if target_type == "real":
            fake = False
            ruin = False
        elif target_type == "fake":
            fake = True
            ruin = False
        else:
            fake = False
            ruin = True
        village: VillageModel = VillageModel.objects.select_related().get(
            coord=coord, world=self.world
        )
        TargetVertex.objects.create(
            outline=self,
            player=village.player.name if village.player else "",
            player_created_at=(
                village.player.created_at if village.player else timezone.now()
            ),
            player_id=village.player.player_id if village.player else None,
            village_id=village.village_id,
            target=coord,
            fake=fake,
            ruin=ruin,
        )

    def is_target_with_no_time(self) -> bool:
        from base.models import TargetVertex

        return (
            TargetVertex.objects.filter(outline=self)
            .filter(outline_time=None)
            .annotate(num_of_weights=Count("weightmodel"))
            .filter(num_of_weights__gt=0)
            .exists()
        )

    def get_outline_times(self):
        from base.models import OutlineTime, PeriodModel

        outline_time_lst = OutlineTime.objects.filter(outline=self).order_by("order")
        period_model_lst = (
            PeriodModel.objects.select_related("outline_time")
            .filter(outline_time__in=outline_time_lst)
            .order_by("from_time", "-unit")
        )

        result: dict[OutlineTime, list[PeriodModel]] = {}
        period: PeriodModel
        for period in period_model_lst:
            if period.outline_time in result:
                result[period.outline_time].append(period)
            else:
                result[period.outline_time] = [period]
        return {
            key: result[key]
            for key in sorted(
                result.keys(), key=lambda outline_time: outline_time.order
            )
        }

    def create_stats(self):
        from base.models import Stats

        Stats.objects.create(
            outline=self,
            outline_pk=self.pk,
            owner_name=self.owner.username,
            world=str(self.world),
            premium_user=self.owner.profile.is_premium(),  # type: ignore
        )

    @property
    def actions(self):
        from utils.basic.outline_stats import action

        return action
