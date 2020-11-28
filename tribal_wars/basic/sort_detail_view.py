from django.core.paginator import Paginator
from django.db.models import F, ExpressionWrapper, FloatField

from base import models


class SortAndPaginRequest:
    def __init__(self, outline, GET_request: str, PAGE_request, target):
        self.outline = outline
        self.target = target.target
        self.x_coord = target.coord_tuple()[0]
        self.y_coord = target.coord_tuple()[1]
        self.page = PAGE_request
        VALID = [
            "distance",
            "-distance",
            "-off_left",
            "-nobleman_left",
            "closest_offs",
            "farthest_offs",
            "closest_noblemans",
            "farthest_noblemans",
            "closest_noble_offs",
            "farthest_noble_offs",
        ]
        if GET_request is None:
            self.sort = "distance"
        if GET_request in VALID:
            self.sort = GET_request
        else:
            self.sort = "distance"

    def __nonused(self): 
        nonused_vertices = (
            models.WeightMaximum.objects.filter(outline=self.outline)
            .exclude(off_left=0, nobleman_left=0)
            .filter(
                off_left__gte=self.outline.filter_weights_min,
                off_left__lte=self.outline.filter_weights_max,
            )
        )
        if self.outline.filter_hide_front == "back":
            nonused_vertices = nonused_vertices.filter(first_line=False)
        if self.outline.filter_hide_front == "front":
            nonused_vertices = nonused_vertices.filter(first_line=True)

        return nonused_vertices

    def __pagin(self, lst_or_query):
        paginator = Paginator(lst_or_query, int(self.outline.filter_card_number))
        page_obj = paginator.get_page(self.page)
        return page_obj

    def sorted_query(self):
        query = self.__nonused()

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

            return self.__pagin(query)

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
            return self.__pagin(query)

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

            return self.__pagin(query)

        elif self.sort == "closest_offs":
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
            ).order_by("distance")

            return self.__pagin(query)

        elif self.sort == "farthest_offs":
            query = (
                query.filter(
                    off_left__gte=self.outline.initial_outline_min_off
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

            return self.__pagin(query)

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
            return self.__pagin(query)

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

            return self.__pagin(query)

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

            return self.__pagin(query)

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

            return self.__pagin(query)

