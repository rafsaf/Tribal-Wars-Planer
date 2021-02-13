from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from base.models import TargetVertex, OutlineTime


class TargetTimeUpdate(APIView):
    """
    For given target id match it with Time obj id.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, target_id, time_id, format=None):
        target = get_object_or_404(TargetVertex, pk=target_id)
        outline_time: OutlineTime = get_object_or_404(
            OutlineTime.objects.select_related(), pk=time_id
        )
        
        if outline_time.outline.owner != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if target.outline_time is None:
            old_id = "none"
        else:
            old_id = f"{target.pk}-time-{target.outline_time.pk}"

        target.outline_time = outline_time
        target.save()

        return Response({"new": f"{target.pk}-time-{time_id}", "old": old_id}, status=status.HTTP_200_OK)

