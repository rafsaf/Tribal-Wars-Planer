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
from django.http.response import HttpResponse

import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import prometheus_client

from base.models import (
    Outline,
    OutlineTime,
    Overview,
    Payment,
    Profile,
    TargetVertex,
    WeightMaximum,
    WeightModel,
)
from rest_api import serializers
from rest_api.permissions import (
    MetricsExportSecretPermission,
    StripeWebhookSafeListPermission,
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
        get_object_or_404(Outline, owner=request.user, pk=target.outline.pk)

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
        get_object_or_404(Outline, id=outline_id, owner=request.user)
        overview: Overview = get_object_or_404(Overview, token=token)

        new_state: bool = not bool(overview.show_hidden)
        name: str
        new_class: str
        if new_state:
            name = "True"
            new_class = "btn btn-light btn-light-no-border md-blue"
        else:
            name = "False"
            new_class = "btn btn-light btn-light-no-border md-error"

        overview.show_hidden = new_state
        overview.save()
        return Response({"name": name, "class": new_class}, status=status.HTTP_200_OK)


class ChangeWeightModelBuilding(APIView):
    """
    For given weight model updates its building.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, outline_id: int, weight_id: int, format=None) -> Response:
        get_object_or_404(Outline, pk=outline_id, owner=request.user)
        weight: WeightModel = get_object_or_404(WeightModel, pk=weight_id)

        building_serializer: serializers.ChangeWeightBuildingSerializer = (
            serializers.ChangeWeightBuildingSerializer(data=request.data)
        )
        if building_serializer.is_valid():
            building: str = building_serializer.validated_data[  # type: ignore
                "building"
            ]
            weight.building = building
            weight.save()
            weight.refresh_from_db()
            new_building: str = weight.get_building_display()  # type: ignore
            return Response({"name": new_building}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ChangeBuildingsArray(APIView):
    """
    For given outline updates array with buildings.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, outline_id: int, format=None) -> Response:
        outline: Outline = get_object_or_404(Outline, id=outline_id, owner=request.user)

        buildings_serializer: serializers.ChangeBuildingsArraySerializer = (
            serializers.ChangeBuildingsArraySerializer(data=request.data)
        )
        if buildings_serializer.is_valid():
            outline.initial_outline_buildings = buildings_serializer.validated_data[  # type: ignore
                "buildings"
            ]
            outline.actions.form_building_order_change(outline)
            outline.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ResetUserMessages(APIView):
    """
    For given outline updates array with buildings.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request: HttpRequest, format=None) -> Response:
        profile: Profile = get_object_or_404(Profile, user=request.user)
        profile.messages = 0
        profile.save()
        return Response(status=status.HTTP_200_OK)


class StripeConfig(APIView):
    """Stripe config endpoint"""

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, format=None) -> Response:
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return Response(stripe_config, status=status.HTTP_200_OK)


class StripeCheckoutSession(APIView):
    """Stripe checkout session endpoint"""

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, amount: int, format=None) -> Response:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if amount not in [30, 55, 70]:
            return Response(status=400)
        price_id: str = settings.STRIPE_PAYMENTS[amount]
        host = request.get_host()
        user_pk: int = request.user.pk
        http = "http://"
        success = reverse("base:payment_done")
        cancel = reverse("base:premium")
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=f"{http}{host}{success}",
                cancel_url=f"{http}{host}{cancel}",
                client_reference_id=user_pk,
                payment_method_types=["card", "p24"],
                mode="payment",
                line_items=[
                    {
                        "quantity": 1,
                        "price": price_id,
                    }
                ],
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            session_id = checkout_session["id"]  # type: ignore
            return Response({"sessionId": session_id}, status=status.HTTP_200_OK)


class StripeWebhook(APIView):
    """Stripe checkout session endpoint"""

    permission_classes = [AllowAny, StripeWebhookSafeListPermission]

    def post(self, request: HttpRequest, format=None) -> Response:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        if sig_header is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            # Invalid payload
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:  # type: ignore
            # Invalid signature
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            evt_id: str = event["id"]
            if not Payment.objects.filter(event_id=evt_id).exists():
                data: dict = event["data"]["object"]
                user: User = User.objects.get(pk=data["client_reference_id"])
                current_date: datetime.date = timezone.localdate()
                months: int = 0
                amount: int = int(data["amount_total"]) // 100

                if amount == 70:
                    months = 3
                elif amount == 55:
                    months = 2
                elif amount == 30:
                    months = 1
                else:
                    raise ValueError("Not known amount of money")
                Payment.objects.create(
                    user=user,
                    amount=amount,
                    from_stripe=True,
                    months=months,
                    payment_date=current_date,
                    event_id=evt_id,
                )
            return Response(status=200)
        return Response(status=404)


class MetricsExport(APIView):

    permission_classes = [AllowAny, MetricsExportSecretPermission]

    def get(self, request: HttpRequest, format=None):
        metrics_page = prometheus_client.generate_latest(prometheus_client.REGISTRY)
        return Response(
            metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST, status=200
        )
