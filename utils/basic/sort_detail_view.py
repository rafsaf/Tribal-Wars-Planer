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

from typing import Optional, Set

from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField, Q

from base import models
from base.models import Outline, TargetVertex


class SortAndPaginRequest:
    VALID_SORT_LIST: Set[str] = {
        "distance",
        "random_distance",
        "-distance",
        "-off_left",
        "-nobleman_left",
        "closest_offs",
        "random_offs",
        "farthest_offs",
        "closest_noblemans",
        "random_noblemans",
        "farthest_noblemans",
        "closest_noble_offs",
        "random_noble_offs",
        "farthest_noble_offs",
    }

    def __init__(
        self,
        outline: Outline,
        request_GET_sort: Optional[str],
        request_GET_page: Optional[str],
        request_GET_filtr: Optional[str],
        target: TargetVertex,
    ):
        self.outline: Outline = outline
        self.target: str = target.target
        self.x_coord: int = target.coord_tuple()[0]
        self.y_coord: int = target.coord_tuple()[1]
        self.page: Optional[str] = request_GET_page
        self.filtr: str = request_GET_filtr or ""

        if request_GET_sort is None:
            self.sort = "distance"
        if request_GET_sort in self.VALID_SORT_LIST:
            self.sort = request_GET_sort
        else:
            self.sort = "distance"

        if self.sort != self.outline.choice_sort:
            self.outline.choice_sort = self.sort
            self.outline.save()

    def _nonused(self):
        query = (
            models.WeightMaximum.objects.filter(outline=self.outline)
            .exclude(off_left=0, nobleman_left=0)
            .filter(
                off_left__gte=self.outline.filter_weights_min,
                off_left__lte=self.outline.filter_weights_max,
                catapult_left__gte=self.outline.filter_weights_catapults_min,
            )
        )
        if self.filtr != "":
            if "|" in self.filtr:
                query = query.filter(start__icontains=self.filtr)
            elif self.filtr.isnumeric() and len(self.filtr) <= 3:
                query = query.filter(
                    Q(start__icontains=self.filtr) | Q(player__icontains=self.filtr)
                )
            else:
                query = query.filter(player__icontains=self.filtr)
        if self.outline.filter_hide_front == "back":
            query = query.filter(first_line=False, too_far_away=False)
        if self.outline.filter_hide_front == "front":
            query = query.filter(first_line=True)
        if self.outline.filter_hide_front == "away":
            query = query.filter(too_far_away=True)

        if self.outline.filter_hide_front == "hidden":
            query = query.filter(hidden=True)
        else:
            query = query.filter(hidden=False)

        return query

    def _pagin(self, lst_or_query):
        paginator = Paginator(lst_or_query, int(self.outline.filter_card_number))
        page_obj = paginator.get_page(self.page)
        return page_obj

    def sorted_query(self):
        query = self._nonused()

        if self.sort == "distance":
            query = query.annotate(
                distance=ExpressionWrapper(
                    (
                        (F("x_coord") - self.x_coord) ** 2
                        + (F("y_coord") - self.y_coord) ** 2
                    )
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            ).order_by("distance")

            return self._pagin(query)

        elif self.sort == "random_distance":
            query = query.annotate(
                distance=ExpressionWrapper(
                    (
                        (F("x_coord") - self.x_coord) ** 2
                        + (F("y_coord") - self.y_coord) ** 2
                    )
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            )
            query = query.order_by("?")
            return self._pagin(query)

        elif self.sort in {"-off_left", "-nobleman_left"}:
            query = query.order_by(self.sort).annotate(
                distance=ExpressionWrapper(
                    (
                        (F("x_coord") - self.x_coord) ** 2
                        + (F("y_coord") - self.y_coord) ** 2
                    )
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            )
            return self._pagin(query)

        elif self.sort == "-distance":
            query = query.annotate(
                distance=ExpressionWrapper(
                    (
                        (F("x_coord") - self.x_coord) ** 2
                        + (F("y_coord") - self.y_coord) ** 2
                    )
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            ).order_by("-distance")

            return self._pagin(query)

        elif self.sort == "closest_offs":
            query = (
                query.filter(off_left__gte=self.outline.initial_outline_min_off)
                .annotate(
                    distance=ExpressionWrapper(
                        (
                            (F("x_coord") - self.x_coord) ** 2
                            + (F("y_coord") - self.y_coord) ** 2
                        )
                        ** (1 / 2),
                        output_field=FloatField(max_length=5),
                    )
                )
                .order_by("distance")
            )

            return self._pagin(query)

        elif self.sort == "random_offs":
            query = query.filter(
                off_left__gte=self.outline.initial_outline_min_off
            ).annotate(
                distance=ExpressionWrapper(
                    (
                        (F("x_coord") - self.x_coord) ** 2
                        + (F("y_coord") - self.y_coord) ** 2
                    )
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            )
            query = query.order_by("?")
            return self._pagin(query)

        elif self.sort == "farthest_offs":
            query = (
                query.filter(off_left__gte=self.outline.initial_outline_min_off)
                .annotate(
                    distance=ExpressionWrapper(
                        (
                            (F("x_coord") - self.x_coord) ** 2
                            + (F("y_coord") - self.y_coord) ** 2
                        )
                        ** (1 / 2),
                        output_field=FloatField(max_length=5),
                    )
                )
                .order_by("-distance")
            )

            return self._pagin(query)

        elif self.sort == "closest_noblemans":
            query = (
                query.filter(nobleman_left__gte=1)
                .annotate(
                    distance=ExpressionWrapper(
                        (
                            (F("x_coord") - self.x_coord) ** 2
                            + (F("y_coord") - self.y_coord) ** 2
                        )
                        ** (1 / 2),
                        output_field=FloatField(max_length=5),
                    )
                )
                .order_by("distance")
            )
            return self._pagin(query)

        elif self.sort == "random_noblemans":
            query = query.filter(nobleman_left__gte=1).annotate(
                distance=ExpressionWrapper(
                    (
                        (F("x_coord") - self.x_coord) ** 2
                        + (F("y_coord") - self.y_coord) ** 2
                    )
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            )
            query = query.order_by("?")
            return self._pagin(query)

        elif self.sort == "farthest_noblemans":
            query = (
                query.filter(nobleman_left__gte=1)
                .annotate(
                    distance=ExpressionWrapper(
                        (
                            (F("x_coord") - self.x_coord) ** 2
                            + (F("y_coord") - self.y_coord) ** 2
                        )
                        ** (1 / 2),
                        output_field=FloatField(max_length=5),
                    )
                )
                .order_by("-distance")
            )

            return self._pagin(query)

        elif self.sort == "closest_noble_offs":
            query = (
                query.filter(
                    nobleman_left__gte=1,
                    off_left__gte=self.outline.initial_outline_min_off,
                )
                .annotate(
                    distance=ExpressionWrapper(
                        (
                            (F("x_coord") - self.x_coord) ** 2
                            + (F("y_coord") - self.y_coord) ** 2
                        )
                        ** (1 / 2),
                        output_field=FloatField(max_length=5),
                    )
                )
                .order_by("distance")
            )

            return self._pagin(query)

        elif self.sort == "random_noble_offs":
            query = query.filter(
                nobleman_left__gte=1,
                off_left__gte=self.outline.initial_outline_min_off,
            ).annotate(
                distance=ExpressionWrapper(
                    (
                        (F("x_coord") - self.x_coord) ** 2
                        + (F("y_coord") - self.y_coord) ** 2
                    )
                    ** (1 / 2),
                    output_field=FloatField(max_length=5),
                )
            )
            query = query.order_by("?")

            return self._pagin(query)

        elif self.sort == "farthest_noble_offs":
            query = (
                query.filter(
                    nobleman_left__gte=1,
                    off_left__gte=self.outline.initial_outline_min_off,
                )
                .annotate(
                    distance=ExpressionWrapper(
                        (
                            (F("x_coord") - self.x_coord) ** 2
                            + (F("y_coord") - self.y_coord) ** 2
                        )
                        ** (1 / 2),
                        output_field=FloatField(max_length=5),
                    )
                )
                .order_by("-distance")
            )

            return self._pagin(query)
