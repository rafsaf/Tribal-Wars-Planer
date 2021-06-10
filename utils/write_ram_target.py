from random import sample
from statistics import mean
from typing import Generator, List, Optional

from django.db.models import (
    Case,
    DecimalField,
    ExpressionWrapper,
    F,
    FloatField,
    IntegerField,
    Q,
    Value,
    When,
)
from django.db.models.functions import Mod
from django.db.models.query import QuerySet

from base.models import Outline
from base.models import TargetVertex as Target
from base.models import WeightMaximum, WeightModel
from utils.basic.ruin import RuinHandle


class WriteRamTarget:
    """
    Single step in making auto outline for given target
    Only OFF, FAKE OFF, RUIN ATTACK

    if self.ruin is True, we assume that ONLY ruin attacks are there

    1. Quering self.default_query (get WeightMaximum, first query)
    Result depend on targets specifications

    2. Then update states (update WeightMaximum, second query)

    3. Finally return List[WeightModel] ready to create orders
    """

    def __init__(
        self,
        target: Target,
        outline: Outline,
        ruin: bool = False,
    ):
        self.target: Target = target
        self.outline: Outline = outline
        self.index: int = 0
        self.default_query: "QuerySet[WeightMaximum]" = WeightMaximum.objects.filter(
            outline=self.outline, too_far_away=False
        )
        self.ruin: bool = ruin
        self.ruin_handle: Optional[RuinHandle] = None
        self.building_generator: Optional[Generator] = None

    def sorted_weights_offs(self, catapults: int = 50) -> List[WeightMaximum]:
        if self.target.fake:
            self._set_fake_query()
        elif self.ruin:
            self._set_ruin_query(catapults=catapults)
        else:
            self._set_off_query()

        self._annotate_distance_on_query()

        if not self.target.mode_off == "closest" and self.target.night_bonus:
            self._add_night_bonus_annotations()

        if self.target.mode_off == "closest":
            self.index = 30000
            if self.ruin:
                self.index += 40000
            return self._closest_weight_lst()

        elif self.target.mode_off == "close":
            self.index = 20000
            if self.ruin:
                self.index += 40000
            return self._close_weight_lst()

        elif self.target.mode_off == "random":
            self.index = 10000
            if self.ruin:
                self.index += 40000
            return self._random_weight_lst()

        else:  # self.target.mode_off == "far":
            self.index = 0
            if self.ruin:
                self.index += 40000
            return self._far_weight_lst()

    def weight_create_list(self) -> List[WeightModel]:

        weights_max_update_lst: List[WeightMaximum] = []
        weights_create_lst: List[WeightModel] = []
        self._set_building_generator()
        if self.ruin:
            off_lst: List[WeightMaximum] = list(
                set(self.sorted_weights_offs(50) + self.sorted_weights_offs(100))
            )
            off_lst.sort(key=lambda weight: -weight.catapult_left)
            off_lst = off_lst[: self.target.required_off]
            off_lst.sort(key=lambda weight: -weight.distance)  # type: ignore
        else:
            off_lst: List[WeightMaximum] = self.sorted_weights_offs()
        i: int
        weight_max: WeightMaximum
        for i, weight_max in enumerate(off_lst):
            try:
                catapult: int = self._catapult(weight_max)
            except StopIteration:
                break
            off: int = self._off(weight_max, catapult)
            building: Optional[str] = self._building()
            fake_limit: int = self._fake_limit()

            weight = self._weight_model(weight_max, off, catapult, building, i)
            weights_create_lst.append(weight)

            weights_max_update_lst.append(
                self._updated_weight_max(weight_max, off, catapult, fake_limit)
            )

        if self.ruin:
            WeightMaximum.objects.bulk_update(
                weights_max_update_lst,
                fields=[
                    "off_state",
                    "off_left",
                    "catapult_state",
                    "catapult_left",
                ],
            )
        elif self.target.fake and len(weights_max_update_lst) > 0:
            WeightMaximum.objects.filter(
                pk__in=[i.pk for i in weights_max_update_lst]
            ).update(
                fake_limit=F("fake_limit") - 1,
                off_state=F("off_state") + 100,
                off_left=F("off_left") - 100,
            )
        else:
            if len(weights_max_update_lst) > 0:
                WeightMaximum.objects.filter(
                    pk__in=[i.pk for i in weights_max_update_lst]
                ).update(
                    off_state=F("off_left") + F("off_state"),
                    catapult_state=F("catapult_left") + F("catapult_state"),
                    catapult_left=0,
                    off_left=0,
                )

        return weights_create_lst

    def _set_building_generator(self) -> None:
        if self.ruin and len(self.outline.initial_outline_buildings) > 0:
            ruin_handle: RuinHandle = RuinHandle(outline=self.outline)
            self.ruin_handle = ruin_handle

    def _building(self) -> Optional[str]:
        if self.ruin_handle is not None:
            building: str = self.ruin_handle.building()
            return building
        return None

    def _off(self, weight_max: WeightMaximum, catapult: int) -> int:
        if self.target.fake:
            return 100
        elif self.ruin:
            return catapult * 8
        else:  # real
            return weight_max.off_left

    def _fake_limit(self) -> int:
        if self.target.fake:
            return 1
        else:
            return 0

    def _catapult(self, weight_max: WeightMaximum) -> int:
        if self.target.fake:
            return 0
        elif self.ruin:
            return self.ruin_handle.best_catapult(weight_max)
        else:  # real
            return weight_max.catapult_left

    def _weight_model(
        self,
        weight_max: WeightMaximum,
        off: int,
        catapult: int,
        building: Optional[str],
        order: int,
    ) -> WeightModel:

        return WeightModel(
            target=self.target,
            player=weight_max.player,
            start=weight_max.start,
            state=weight_max,
            off=off,
            catapult=catapult,
            ruin=self.ruin,
            building=building,
            distance=weight_max.distance,  # type: ignore
            nobleman=0,
            order=order + self.index,
            first_line=weight_max.first_line,
        )

    @staticmethod
    def _updated_weight_max(
        weight_max: WeightMaximum, off: int, catapult: int, fake_limit: int
    ) -> WeightMaximum:
        weight_max.off_state += off
        weight_max.off_left -= off
        weight_max.catapult_state += catapult
        weight_max.catapult_left -= catapult
        weight_max.fake_limit -= fake_limit

        return weight_max

    def _set_fake_query(self) -> None:
        if self.outline.initial_outline_fake_mode == "off":
            self.default_query = self.default_query.filter(
                fake_limit__gte=1,
                off_left__gte=self.outline.initial_outline_min_off,
            )
        else:
            self.default_query = self.default_query.filter(
                fake_limit__gte=1,
                off_left__gte=100 + F("catapult_left") * 8,
            )

    def _set_ruin_query(self, catapults=50) -> None:
        self.default_query = self.default_query.filter(
            Q(
                catapult_left__gte=catapults,
                off_left__lt=self.outline.initial_outline_min_off,
            )
            | Q(
                catapult_left__gte=catapults
                + self.outline.initial_outline_off_left_catapult,
                off_left__gte=self.outline.initial_outline_min_off,
            )
        )

    def _set_off_query(self) -> None:
        self.default_query = self.default_query.filter(
            off_left__gte=self.outline.initial_outline_min_off,
        )

    def _annotate_distance_on_query(self) -> None:
        x_coord: int = self.target.coord_tuple()[0]
        y_coord: int = self.target.coord_tuple()[1]

        self.default_query = self.default_query.annotate(
            distance=ExpressionWrapper(
                ((F("x_coord") - x_coord) ** 2 + (F("y_coord") - y_coord) ** 2)
                ** (1 / 2),
                output_field=DecimalField(max_digits=2),
            )
        ).filter(distance__lte=self.outline.initial_outline_maximum_front_dist)

    def _add_night_bonus_annotations(self) -> None:
        avg_dist: float = mean((self.target.enter_t1, self.target.enter_t2))
        interval_dist: int = self.target.enter_t2 - avg_dist
        dividier: int = (
            self.outline.world.speed_world * self.outline.world.speed_units * 2
        )

        self.default_query = (
            self.default_query.annotate(
                time_hours=ExpressionWrapper(
                    (F("distance") / dividier),
                    output_field=FloatField(),
                )
            )
            .annotate(
                time_mod=Mod(
                    "time_hours",
                    Value("24", output_field=FloatField()),
                    output_field=FloatField(),
                )
            )
            .annotate(
                night_score=Mod(
                    avg_dist - F("time_mod") + 24,
                    Value("24", output_field=FloatField()),
                    output_field=FloatField(),
                ),
            )
            .annotate(
                night_bool=Case(
                    When(
                        night_score__gte=7 + interval_dist,
                        night_score__lte=24 - interval_dist,
                        then=3,
                    ),
                    When(night_score__gte=7, night_score__lte=24, then=2),
                    default=Value("1"),
                    output_field=IntegerField(),
                )
            )
        )

    def _closest_weight_lst(self) -> List[WeightMaximum]:
        weight_list: List[WeightMaximum] = list(
            self.default_query.order_by("distance")[: 1 * self.target.required_off]
        )
        weight_list.sort(key=lambda weight: -weight.distance)  # type: ignore
        return weight_list

    def _close_weight_lst(self) -> List[WeightMaximum]:
        self.default_query = self.default_query.filter(
            first_line=False,
            distance__gte=self.outline.initial_outline_front_dist,
        )
        if self.target.night_bonus:
            self.default_query = self.default_query.order_by("-night_bool", "distance")
        else:
            self.default_query = self.default_query.order_by("distance")
        weight_list: List[WeightMaximum] = list(
            self.default_query[: 2 * self.target.required_off]
        )

        if len(weight_list) < self.target.required_off:
            required: int = len(weight_list)
        else:
            required: int = self.target.required_off

        sampled_weight_lst: List[WeightMaximum] = sample(weight_list, required)

        return sorted(
            sampled_weight_lst,
            key=lambda item: item.distance,  # type: ignore
            reverse=True,
        )

    def _random_query(self, night_bool: Optional[int]) -> "QuerySet[WeightMaximum]":
        queryset: "QuerySet[WeightMaximum]" = self.default_query.filter(
            first_line=False,
            distance__gte=self.outline.initial_outline_front_dist,
        )
        if night_bool is not None:
            queryset = queryset.filter(night_bool=night_bool)
        return queryset.order_by("?")

    def _random_weight_lst(self) -> List[WeightMaximum]:
        if self.target.night_bonus:
            result_lst: List[WeightMaximum] = []
            left_offs: int = self.target.required_off

            weight_list_3: List[WeightMaximum] = list(
                self._random_query(night_bool=3)[:left_offs]
            )

            result_lst += weight_list_3
            left_offs -= len(weight_list_3)

            if left_offs > 0:

                weight_list_2: List[WeightMaximum] = list(
                    self._random_query(night_bool=2)[:left_offs]
                )

                result_lst += weight_list_2
                left_offs -= len(weight_list_2)

                if left_offs > 0:

                    weight_list_1: List[WeightMaximum] = list(
                        self._random_query(night_bool=1)[:left_offs]
                    )

                    result_lst += weight_list_1
                    left_offs -= len(weight_list_1)

        else:
            result_lst: List[WeightMaximum] = list(
                self._random_query(night_bool=None)[: self.target.required_off]
            )

        return sorted(
            result_lst,
            key=lambda item: item.distance,  # type: ignore
            reverse=True,
        )

    def _far_weight_lst(self) -> List[WeightMaximum]:
        self.default_query = self.default_query.filter(
            first_line=False,
            distance__gte=self.outline.initial_outline_front_dist,
        )
        if self.target.night_bonus:
            self.default_query = self.default_query.order_by("-night_bool", "-distance")
        else:
            self.default_query = self.default_query.order_by("-distance")

        weight_list: List[WeightMaximum] = list(
            self.default_query[: 3 * self.target.required_off]
        )
        if len(weight_list) < self.target.required_off:
            required: int = len(weight_list)
        else:
            required: int = self.target.required_off

        sampled_weight_lst: List[WeightMaximum] = sample(weight_list, required)

        return sorted(
            sampled_weight_lst,
            key=lambda item: item.distance,  # type: ignore
            reverse=True,
        )
