from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from base.models import TargetVertex, OutlineTime, Outline, WeightModel, WeightMaximum


class TargetTimeUpdate(APIView):
    """
    For given target id match it with Time obj id.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, target_id, time_id, format=None):
        target = get_object_or_404(TargetVertex, pk=target_id)
        outline_time: OutlineTime = get_object_or_404(
            OutlineTime.objects.select_related("outline"), pk=time_id
        )

        if outline_time.outline.owner != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
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

    def delete(self, request, target_id, format=None):
        target: TargetVertex = get_object_or_404(
            TargetVertex.objects.select_related("outline"), pk=target_id
        )
        outline: Outline = get_object_or_404(
            Outline, owner=request.user, pk=target.outline.pk
        )

        weights = WeightModel.objects.select_related("state").filter(target=target)
        # deletes weights related to this target and updates weight state
        state_updates = []
        for weight_model in weights:
            weight_model.state.off_left += weight_model.off
            weight_model.state.off_state -= weight_model.off
            weight_model.state.nobleman_left += weight_model.nobleman
            weight_model.state.nobleman_state -= weight_model.nobleman
            state_updates.append(weight_model.state)

        WeightMaximum.objects.bulk_update(
            state_updates, ["off_left", "off_state", "nobleman_left", "nobleman_state"]
        )
        weights.delete()
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)