from random import sample
from statistics import mean
from typing import Generator, List
from tribal_wars.basic.ruin import RuinHandle

from django.db.models import (
    F,
    Q,
    DecimalField,
    ExpressionWrapper,
    IntegerField,
    Value,
    FloatField,
    Case,
    When,
)
from django.db.models.functions import Mod
from base import models


class WriteTarget:
    def __init__(
        self,
        target: models.TargetVertex,
        outline: models.Outline,
        world: models.World,
        ruin: bool=False,
    ):
        self.target: models.TargetVertex = target
        self.x_coord: int = target.coord_tuple()[0]
        self.y_coord: int = target.coord_tuple()[1]
        self.outline: models.Outline = outline
        self.ruin: bool = ruin
        self.end_up_offs: bool = False
        self.end_up_nobles: bool = False
        self.index: int = 0
        
        self.avg_dist: float = mean((self.target.enter_t1, self.target.enter_t2))
        self.interval_dist: int = self.target.enter_t2 - self.avg_dist
        self.dividier: int = world.speed_world * world.speed_units * 2

    def write_noble(self):
        weights_max_update_lst: List[models.WeightMaximum] = []
        weights_create_lst: List[models.WeightModel] = []

        nobles_weight_max = self.sorted_weights_noble()
        available = sum([weight.nobleman_left for weight in nobles_weight_max])
        if available == 0:
            if self.target.mode_noble == "closest":
                self.end_up_nobles = True
                return None
            self.target.mode_noble = "finished_back"
            nobles_weight_max = self.sorted_weights_noble()
            available = sum([weight.nobleman_left for weight in nobles_weight_max])
            if available == 0:
                self.end_up_nobles = True
                return None

        choosen_by_the_god = (
            []
        )  # list with (weight_max, number_of_nobles_to_write) tuples

        if self.target.mode_guide == "one":  # one weight-one target prefer

            while self.target.required_noble > 0 and len(nobles_weight_max) > 0:
                exact = sorted(
                    [
                        weight
                        for weight in nobles_weight_max
                        if weight.nobleman_left >= self.target.required_noble
                    ],
                    key=lambda weight: (-weight.off_left, -weight.distance),
                )
                if (
                    len(exact) > 0
                ):  # there is a village with exact OR more number of nobles than required
                    choosen_by_the_god.append((exact[0], self.target.required_noble))
                    self.target.required_noble = 0
                else:
                    nobles_weight_max.sort(
                        key=lambda weight: (-weight.off_left, -weight.distance)
                    )
                    to_add = nobles_weight_max.pop(0)
                    choosen_by_the_god.append((to_add, to_add.nobleman_left))
                    self.target.required_noble -= to_add.nobleman_left

        elif self.target.mode_guide == "many":  # optimal- one or many prefer
            nobles_weight_max.sort(
                key=lambda weight: (-weight.off_left, -weight.distance)
            )
            while self.target.required_noble > 0 and len(nobles_weight_max) > 0:
                to_add = nobles_weight_max.pop(0)
                noble_to_add = min(to_add.nobleman_left, self.target.required_noble)
                self.target.required_noble -= noble_to_add
                choosen_by_the_god.append((to_add, noble_to_add))

        elif self.target.mode_guide == "single":  # only single nobles
            nobles_weight_max.sort(
                key=lambda weight: (-weight.off_left, -weight.distance)
            )
            while self.target.required_noble > 0 and len(nobles_weight_max) > 0:
                to_add = nobles_weight_max.pop(0)
                self.target.required_noble -= 1
                choosen_by_the_god.append((to_add, 1))

        i: int = 0
        weight_max: models.WeightMaximum
        noble_number: int
        for weight_max, noble_number in choosen_by_the_god:
            if self.target.fake:
                off = 0
                big_off = 0
                to_left = weight_max.off_left

            elif weight_max.off_left < 200 * weight_max.nobleman_left:
                off = weight_max.off_left // weight_max.nobleman_left
                big_off = weight_max.off_left - (off * (weight_max.nobleman_left - 1))
                if weight_max.nobleman_left > noble_number:
                    to_left = off * (weight_max.nobleman_left - noble_number)
                else:
                    to_left = 0

            elif self.target.mode_division == "divide":

                off = weight_max.off_left // weight_max.nobleman_left
                big_off = weight_max.off_left - (off * (weight_max.nobleman_left - 1))
                if weight_max.nobleman_left > noble_number:
                    to_left = off * (weight_max.nobleman_left - noble_number)
                else:
                    to_left = 0

            elif self.target.mode_division == "not_divide":
                if weight_max.nobleman_left > noble_number:
                    to_left = 200 * (weight_max.nobleman_left - noble_number)
                else:
                    to_left = 0
                off = 200
                big_off = weight_max.off_left - (off * (weight_max.nobleman_left - 1))

            else:  # self.target.mode_division == "separatly":
                off = 200
                big_off = 200
                to_left = weight_max.off_left - (off * (noble_number))

            if self.outline.mode_split == "split":
                for _ in range(noble_number):
                    if _ == 0:
                        off_troops = big_off
                    else:
                        off_troops = off

                    weight = models.WeightModel(
                        target=self.target,
                        player=weight_max.player,
                        start=weight_max.start,
                        state=weight_max,
                        off=off_troops,
                        distance=weight_max.distance,
                        nobleman=1,
                        order=i + self.index,
                        first_line=weight_max.first_line,
                    )
                    i += 1
                    weights_create_lst.append(weight)
            else:  # self.outline.mode_split == "together":
                weight = models.WeightModel(
                    target=self.target,
                    player=weight_max.player,
                    start=weight_max.start,
                    state=weight_max,
                    off=big_off + (noble_number - 1) * off,
                    distance=weight_max.distance,
                    nobleman=noble_number,
                    order=i + self.index,
                    first_line=weight_max.first_line,
                )
                i += 1
                weights_create_lst.append(weight)

            weight_max.off_state += weight_max.off_left - to_left
            weight_max.off_left = to_left
            weight_max.nobleman_state += noble_number
            weight_max.nobleman_left = weight_max.nobleman_left - noble_number

            weights_max_update_lst.append(weight_max)

        models.WeightMaximum.objects.bulk_update(
            weights_max_update_lst,
            fields=[
                "off_state",
                "off_left",
                "nobleman_state",
                "nobleman_left",
            ],
        )
        models.WeightModel.objects.bulk_create(weights_create_lst)

    def write_ram(self):
        weights_max_update_lst = []
        weights_create_lst = []
        if self.ruin:
            ruin_handle: RuinHandle = RuinHandle(outline=self.outline)
            ruin_iter: Generator = ruin_handle.yield_building()

        weight_max: models.WeightMaximum
        for i, weight_max in enumerate(self.sorted_weights_offs()):
            building = None
            if self.target.fake:
                off = 100
                fake_limit = 1
                catapult = 0
            elif self.ruin:
                off = self.outline.initial_outline_catapult_default * 8
                catapult = self.outline.initial_outline_catapult_default
                fake_limit = 0
                try: 
                    building = next(ruin_iter)
                except StopIteration:
                    break
            else:
                off = weight_max.off_left
                catapult = weight_max.catapult_left
                fake_limit = 0

            weight = models.WeightModel(
                target=self.target,
                player=weight_max.player,
                start=weight_max.start,
                state=weight_max,
                off=off,
                catapult=catapult,
                ruin=self.ruin,
                building=building,
                distance=weight_max.distance,
                nobleman=0,
                order=i + self.index,
                first_line=weight_max.first_line,
            )

            weight_max.off_state += off
            weight_max.off_left -= off
            weight_max.catapult_state += catapult
            weight_max.catapult_left -= catapult
            weight_max.fake_limit -= fake_limit

            weights_create_lst.append(weight)
            weights_max_update_lst.append(weight_max)

        models.WeightMaximum.objects.bulk_update(
            weights_max_update_lst,
            fields=[
                "off_state",
                "off_left",
                "fake_limit",
                "catapult_state",
                "catapult_left",
            ],
        )
        models.WeightModel.objects.bulk_create(weights_create_lst)

    def sorted_weights_offs(self):
        if self.target.fake:
            if self.outline.initial_outline_fake_mode == "off":
                default_off_query = models.WeightMaximum.objects.filter(
                    fake_limit__gte=1,
                    outline=self.outline,
                    off_left__gte=self.outline.initial_outline_min_off,
                )
            else:
                default_off_query = models.WeightMaximum.objects.filter(
                    fake_limit__gte=1,
                    outline=self.outline,
                    off_left__gte=100 + F("catapult_left") * 8,
                )   
        elif self.ruin:
            default_off_query = models.WeightMaximum.objects.filter(
                outline=self.outline
            ).filter(
                Q(
                    catapult_left__gte=self.outline.initial_outline_catapult_default,
                    off_left__lt=self.outline.initial_outline_min_off,
                )
                | Q(
                    catapult_left__gte=self.outline.initial_outline_catapult_default
                    + self.outline.initial_outline_off_left_catapult,
                    off_left__gte=self.outline.initial_outline_min_off,
                )
            )
        else:
            default_off_query = models.WeightMaximum.objects.filter(
                outline=self.outline,
                off_left__gte=self.outline.initial_outline_min_off,
            )

        default_off_query = default_off_query.annotate(
            distance=ExpressionWrapper(
                (
                    (F("x_coord") - self.x_coord) ** 2
                    + (F("y_coord") - self.y_coord) ** 2
                )
                ** (1 / 2),
                output_field=DecimalField(max_digits=2),
            )
        )
        if not self.target.mode_off == "closest" and self.target.night_bonus:
            default_off_query = (
                default_off_query.annotate(
                    time_hours=ExpressionWrapper(
                        (F("distance") / self.dividier),
                        output_field=FloatField(),
                    )
                )
                .annotate(
                    time_mod=Mod(
                        "time_hours",
                        Value("24", output_field=FloatField()),
                        output_field=FloatField(),
                    ),
                    night_score=Mod(
                        self.avg_dist - F("time_mod") + 24,
                        Value("24", output_field=FloatField()),
                        output_field=FloatField(),
                    ),
                )
                .annotate(
                    night_bool=Case(
                        When(
                            night_score__gte=7 + self.interval_dist,
                            night_score__lte=24 - self.interval_dist,
                            then=3,
                        ),
                        When(night_score__gte=7, night_score__lte=24, then=2),
                        default=Value("1"),
                        output_field=IntegerField(),
                    )
                )
            )

        if self.target.mode_off == "closest":
            self.index = 30000
            if self.ruin:
                self.index += 40000
            weight_list = default_off_query.order_by("distance")[
                : 2 * self.target.required_off
            ]
            if len(weight_list) < self.target.required_off:
                self.end_up_offs = True
            return sorted(
                weight_list,
                key=lambda item: (item.nobleman_left, -item.distance),
            )[: self.target.required_off]

        if self.target.mode_off == "close":
            self.index = 20000
            if self.ruin:
                self.index += 40000
            if self.target.night_bonus:
                weight_list = list(
                    default_off_query.filter(
                        first_line=False,
                        distance__gte=self.outline.initial_outline_front_dist,
                    ).order_by("-night_bool", "distance")[
                        : 2 * self.target.required_off
                    ]
                )
            else:
                weight_list = list(
                    default_off_query.filter(
                        first_line=False,
                        distance__gte=self.outline.initial_outline_front_dist,
                    ).order_by("distance")[: 2 * self.target.required_off]
                )
            if len(weight_list) < self.target.required_off:
                required = len(weight_list)
                self.end_up_offs = True
            else:
                required = self.target.required_off
            return sorted(
                sample(weight_list, required),
                key=lambda item: item.distance,
                reverse=True,
            )

        if self.target.mode_off == "random":
            self.index = 10000
            if self.ruin:
                self.index += 40000
            if self.target.night_bonus:
                weight_list = list(
                    default_off_query.filter(
                        first_line=False,
                        distance__gte=self.outline.initial_outline_front_dist,
                        night_bool=3,
                    ).order_by("?")[: self.target.required_off]
                )
                if len(weight_list) < self.target.required_off:
                    weight_list = list(
                        default_off_query.filter(
                            first_line=False,
                            distance__gte=self.outline.initial_outline_front_dist,
                            night_bool=2,
                        ).order_by("?")[: self.target.required_off]
                    )
                    if len(weight_list) < self.target.required_off:
                        weight_list = list(
                            default_off_query.filter(
                                first_line=False,
                                distance__gte=self.outline.initial_outline_front_dist,
                                night_bool=1,
                            ).order_by("?")[: self.target.required_off]
                        )
                        if len(weight_list) < self.target.required_off:
                            self.end_up_offs = True
                return sorted(
                    weight_list,
                    key=lambda item: item.distance,
                    reverse=True,
                )
            else:
                weight_list = list(
                    default_off_query.filter(
                        first_line=False,
                        distance__gte=self.outline.initial_outline_front_dist,
                    ).order_by("?")[: self.target.required_off]
                )
                if len(weight_list) < self.target.required_off:
                    self.end_up_offs = True

                return sorted(
                    weight_list,
                    key=lambda item: item.distance,
                    reverse=True,
                )

        if self.target.mode_off == "far":
            self.index = 0
            if self.ruin:
                self.index += 40000
            if self.target.night_bonus:
                weight_list = list(
                    default_off_query.filter(
                        first_line=False,
                        distance__gte=self.outline.initial_outline_front_dist,
                    ).order_by("-night_bool", "-distance")[
                        : 3 * self.target.required_off
                    ]
                )
            else:
                weight_list = list(
                    default_off_query.filter(
                        first_line=False,
                        distance__gte=self.outline.initial_outline_front_dist,
                    ).order_by("-distance")[: 3 * self.target.required_off]
                )
            if len(weight_list) < self.target.required_off:
                required = len(weight_list)
                self.end_up_offs = True
            else:
                required = self.target.required_off
            return sorted(
                sample(weight_list, required),
                key=lambda item: item.distance,
                reverse=True,
            )

    def sorted_weights_noble(self):

        default_noble_query = models.WeightMaximum.objects.filter(
            outline=self.outline,
            nobleman_left__gte=1,
            off_left__gte=200,
        )

        default_noble_query = default_noble_query.annotate(
            distance=ExpressionWrapper(
                (
                    (F("x_coord") - self.x_coord) ** 2
                    + (F("y_coord") - self.y_coord) ** 2
                )
                ** (1 / 2),
                output_field=DecimalField(max_digits=2),
            )
        ).filter(distance__lte=self.outline.initial_outline_target_dist)

        if self.target.mode_noble == "finished_back":
            # after there is no nobles back, take front nobles
            self.index = 120000
            weight_list = default_noble_query.order_by("-distance")[:10]
            return sorted(
                weight_list,
                key=lambda item: item.distance,
            )

        if self.target.mode_noble == "closest":
            self.index = 110000
            weight_list = default_noble_query.order_by("distance")[:10]
            return sorted(
                weight_list,
                key=lambda item: item.distance,
            )

        if self.target.mode_noble == "close":
            self.index = 100000
            weight_list = list(
                default_noble_query.filter(
                    first_line=False,
                    distance__gte=self.outline.initial_outline_front_dist,
                ).order_by("distance")[:10]
            )
            return sorted(
                weight_list,
                key=lambda item: item.distance,
            )

        if self.target.mode_noble == "random":
            self.index = 90000
            weight_list = list(
                default_noble_query.filter(
                    first_line=False,
                    distance__gte=self.outline.initial_outline_front_dist,
                ).order_by("?")[:10]
            )
            return sorted(
                weight_list,
                key=lambda item: item.distance,
            )

        if self.target.mode_noble == "far":
            self.index = 80000
            weight_list = list(
                default_noble_query.filter(
                    first_line=False,
                    distance__gte=self.outline.initial_outline_front_dist,
                ).order_by("-distance")[:10]
            )
            return sorted(
                weight_list,
                key=lambda item: item.distance,
            )
