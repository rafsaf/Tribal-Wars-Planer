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


import random

from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField, Q

from base import models
from base.models import Outline, TargetVertex


class SortAndPaginRequest:
    VALID_SORT_LIST: set[str] = {
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
        request_GET_sort: str | None,
        request_GET_page: str | None,
        request_GET_filtr: str | None,
        target: TargetVertex,
        deff_noble_exists: bool = False,
    ):
        self.outline: Outline = outline
        self.target_vertex: TargetVertex = target
        self.target: str = target.target
        self.x_coord: int = target.coord_tuple()[0]
        self.y_coord: int = target.coord_tuple()[1]
        self.page: str | None = request_GET_page
        self.filtr: str = request_GET_filtr or ""
        self.deff_noble_exists = deff_noble_exists

        if request_GET_sort is None:
            self.sort = "distance"
        if request_GET_sort in self.VALID_SORT_LIST:
            self.sort = request_GET_sort
        else:
            self.sort = "distance"

        if self.sort != self.outline.choice_sort:
            self.outline.choice_sort = self.sort
            self.outline.save(update_fields=["choice_sort"])

    def _base_nonused(self):
        query = models.WeightMaximum.objects.filter(outline=self.outline).exclude(
            off_left=0,
            nobleman_left=0,
            deff_left=0,
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

    def _nonused(self):
        return self._base_nonused().filter(
            off_left__gte=self.outline.filter_weights_min,
            off_left__lte=self.outline.filter_weights_max,
            catapult_left__gte=self.outline.filter_weights_catapults_min,
            nobleman_left__gte=self.outline.filter_weights_nobles_min,
        )

    def _use_deff_target_candidates(self) -> bool:
        return self.target_vertex.has_deff_noble and not self.deff_noble_exists

    def _matches_off_candidate(self, weight: models.WeightMaximum) -> bool:
        return all(
            [
                weight.off_left >= self.outline.filter_weights_min,
                weight.off_left <= self.outline.filter_weights_max,
                weight.catapult_left >= self.outline.filter_weights_catapults_min,
                weight.nobleman_left >= self.outline.filter_weights_nobles_min,
            ]
        )

    def _matches_deff_candidate(self, weight: models.WeightMaximum) -> bool:
        return all(
            [
                weight.deff_left >= self.outline.filter_weights_deff_min,
                weight.deff_left <= self.outline.filter_weights_deff_max,
                weight.nobleman_left >= max(1, self.outline.filter_weights_nobles_min),
            ]
        )

    def _preferred_candidate_role(self, weight: models.WeightMaximum) -> str | None:
        if weight.deff_max > weight.off_max:
            return "deff"
        if weight.off_max > 0:
            return "off"
        if weight.deff_max > 0:
            return "deff"
        return None

    def _resolve_candidate_role(self, weight: models.WeightMaximum) -> str | None:
        preferred_role = self._preferred_candidate_role(weight)
        if preferred_role == "deff" and self._matches_deff_candidate(weight):
            return "deff"
        if preferred_role == "off" and self._matches_off_candidate(weight):
            return "off"
        return None

    def _annotated_base_query(self):
        return self._base_nonused().annotate(
            distance=ExpressionWrapper(
                (
                    (F("x_coord") - self.x_coord) ** 2
                    + (F("y_coord") - self.y_coord) ** 2
                )
                ** (1 / 2),
                output_field=FloatField(max_length=5),
            )
        )

    def _deff_target_candidates(self):
        candidates = []
        for weight in self._annotated_base_query():
            role = self._resolve_candidate_role(weight)
            if role is None:
                continue
            setattr(weight, "candidate_role", role)
            setattr(
                weight,
                "display_troops",
                weight.deff_left if role == "deff" else weight.off_left,
            )
            candidates.append(weight)
        return candidates

    def _sort_deff_target_candidates(self):
        candidates = self._deff_target_candidates()

        if self.sort in {
            "distance",
            "closest_offs",
            "closest_noblemans",
            "closest_noble_offs",
        }:
            candidates.sort(
                key=lambda weight: (
                    weight.distance,
                    -weight.display_troops,
                    -weight.nobleman_left,
                )
            )
        elif self.sort in {
            "-distance",
            "farthest_offs",
            "farthest_noblemans",
            "farthest_noble_offs",
        }:
            candidates.sort(
                key=lambda weight: (
                    -weight.distance,
                    -weight.display_troops,
                    -weight.nobleman_left,
                )
            )
        elif self.sort == "-off_left":
            candidates.sort(
                key=lambda weight: (
                    -weight.display_troops,
                    weight.distance,
                    -weight.nobleman_left,
                )
            )
        elif self.sort == "-nobleman_left":
            candidates.sort(
                key=lambda weight: (
                    -weight.nobleman_left,
                    weight.distance,
                    -weight.display_troops,
                )
            )
        elif self.sort in {
            "random_distance",
            "random_offs",
            "random_noblemans",
            "random_noble_offs",
        }:
            random.shuffle(candidates)
        else:
            candidates.sort(
                key=lambda weight: (
                    weight.distance,
                    -weight.display_troops,
                    -weight.nobleman_left,
                )
            )

        return self._pagin(candidates)

    def _pagin(self, lst_or_query):
        paginator = Paginator(lst_or_query, int(self.outline.filter_card_number))
        page_obj = paginator.get_page(self.page)
        return page_obj

    def sorted_query(self):  # noqa: PLR0912,PLR0911
        if self._use_deff_target_candidates():
            return self._sort_deff_target_candidates()

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
