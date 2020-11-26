from random import sample

from django.db.models import F, DecimalField, ExpressionWrapper

from base import models
from tribal_wars import basic


class WriteTarget:
    def __init__(self, target: models.TargetVertex, outline: models.Outline):
        self.target = target
        self.x_coord = target.coord_tuple()[0]
        self.y_coord = target.coord_tuple()[1]
        self.outline = outline

    @basic.timing
    def write_ram(self):
        weights_max_update_lst = []
        weights_create_lst = []

        for i, weight_max in enumerate(self.sorted_weights()):
            if self.target.fake:
                off = 100
                fake_limit = 1
            else:
                off = weight_max.off_left
                fake_limit = 0

            weight = models.WeightModel(
                target=self.target,
                player=weight_max.player,
                start=weight_max.start,
                state=weight_max,
                off=off,
                distance=weight_max.distance,
                nobleman=0,
                order=i,
                first_line=weight_max.first_line,
            )

            weight_max.off_state += off
            weight_max.off_left -= off
            weight_max.fake_limit -= fake_limit

            weights_create_lst.append(weight)
            weights_max_update_lst.append(weight_max)

        models.WeightMaximum.objects.bulk_update(
            weights_max_update_lst,
            fields=["off_state", "off_left", "fake_limit"],
        )
        models.WeightModel.objects.bulk_create(weights_create_lst)

    def sorted_weights(self):
        if self.target.fake:
            default_off_query = models.WeightMaximum.objects.filter(
                fake_limit__gte=1,
                outline=self.outline,
                off_left__gte=self.outline.initial_outline_min_off,
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

        if self.target.mode_off == "closest":
            return sorted(
                default_off_query.order_by("distance")[
                    : self.target.required_off
                ],
                key=lambda item: item.distance,
                reverse=True,
            )

        elif self.target.mode_off == "close":
            return sample(
                sorted(
                    default_off_query.filter(
                        distance__gte=self.outline.initial_outline_front_dist
                    ).order_by("distance")[: 2 * self.target.required_off],
                    key=lambda item: item.distance,
                    reverse=True,
                ),
                self.target.required_off,
            )

        elif self.target.mode_off == "random":
            return sorted(
                default_off_query.filter(
                    distance__gte=self.outline.initial_outline_front_dist
                ).order_by("?")[: self.target.required_off],
                key=lambda item: item.distance,
                reverse=True,
            )

        elif self.target.mode_off == "far":
            return sample(
                sorted(
                    default_off_query.filter(
                        distance__gte=self.outline.initial_outline_front_dist
                    ).order_by("-distance")[: 3 * self.target.required_off],
                    key=lambda item: item.distance,
                    reverse=True,
                ),
                self.target.required_off,
            )

