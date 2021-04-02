from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api import serializers

from base.models import (
    TargetVertex,
    OutlineTime,
    Outline,
    WeightModel,
    WeightMaximum,
    Overview,
)


class TargetTimeUpdate(APIView):
    """
    For given target id match it with Time obj id.
    """

    permission_classes = [IsAuthenticated]

    def put(
        self, request: HttpRequest, target_id: int, time_id: int, format=None
    ) -> Response:
        target: TargetVertex = get_object_or_404(TargetVertex, pk=target_id)
        outline_time: OutlineTime = get_object_or_404(
            OutlineTime.objects.select_related("outline"),
            pk=time_id,
            outline__owner=request.user,
        )
        old_id: str

        if target.outline_time is None:
            old_id = "none"
        else:
            old_id = f"{target.pk}-time-{target.outline_time.pk}"

        target.outline_time = outline_time
        target.save()

        return Response(
            {"new": f"{target.pk}-time-{time_id}", "old": old_id},
            status=status.HTTP_200_OK,
        )


class TargetDelete(APIView):
    """
    For given target id, delete obj.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request: HttpRequest, target_id: int, format=None) -> Response:
        target: TargetVertex = get_object_or_404(
            TargetVertex.objects.select_related("outline"), pk=target_id
        )
        outline: Outline = get_object_or_404(
            Outline, owner=request.user, pk=target.outline.pk
        )

        weights = WeightModel.objects.filter(target=target)
        # deletes weights related to this target and updates weight state
        weight_model: WeightModel
        for weight_model in weights:
            state: WeightMaximum = weight_model.state
            state.off_left += weight_model.off
            state.off_state -= weight_model.off
            state.nobleman_left += weight_model.nobleman
            state.nobleman_state -= weight_model.nobleman
            state.catapult_left += weight_model.catapult
            state.catapult_state -= weight_model.catapult
            state.save()

        weights.delete()
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OverwiewStateHideUpdate(APIView):
    """
    For given target id, delete obj.
    """

    permission_classes = [IsAuthenticated]

    def put(
        self, request: HttpRequest, outline_id: int, token: str, format=None
    ) -> Response:
        outline: Outline = get_object_or_404(Outline, id=outline_id, owner=request.user)
        overview: Overview = get_object_or_404(Overview, token=token)

        new_state: bool = not bool(overview.show_hidden)
        name: str
        new_class: str
        if new_state:
            name = "True"
            new_class = "btn btn-light md-blue"
        else:
            name = "False"
            new_class = "btn btn-light md-error"

        overview.show_hidden = new_state
        overview.save()
        return Response({"name": name, "class": new_class}, status=status.HTTP_200_OK)


class ChangeBuildingsArray(APIView):
    """
    For given outline updates array with buildings.
    """

    permission_classes = [IsAuthenticated]

    def put(
        self, request, outline_id: int, format=None
    ) -> Response:
        outline: Outline = get_object_or_404(Outline, id=outline_id, owner=request.user)

        buildings_serializer = serializers.ChangeBuildingsArraySerializer(data=request.data)
        if buildings_serializer.is_valid():
            outline.initial_outline_buildings = buildings_serializer.validated_data["buildings"]
            outline.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
