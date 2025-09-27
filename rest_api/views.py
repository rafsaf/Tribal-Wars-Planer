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
import logging

import prometheus_client
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.translation import activate
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from prometheus_client import multiprocess
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

import metrics
from base import models
from base.management.commands.initstripe import synchronize_stripe
from base.models import (
    Outline,
    OutlineTime,
    Overview,
    Payment,
    Profile,
    StripePrice,
    TargetVertex,
    WeightMaximum,
    WeightModel,
)
from rest_api import serializers
from rest_api.overview_data import get_overview_data, get_overview_data_many
from rest_api.permissions import MetricsExportSecretPermission
from rest_api.serializers import (
    ChangeBuildingsArraySerializer,
    ChangeWeightBuildingSerializer,
    OverwiewStateHideSerializer,
    ShipmentUpdateSendListSerializer,
    StripeSessionAmount,
    TargetDeleteSerializer,
    TargetTimeUpdateSerializer,
)
from shipments.models import Shipment

LANGUAGES: set[str] = set(lang[0] for lang in settings.LANGUAGES)

log = logging.getLogger(__name__)


@extend_schema(
    tags=["internal"],
    responses={200: OpenApiResponse(response=None, description="alive")},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def healthcheck(request: Request):
    return Response(status=status.HTTP_200_OK)


@extend_schema(exclude=True)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def target_time_update(request: Request):
    """
    For given target id match it with Time obj id.
    """
    req = TargetTimeUpdateSerializer(data=request.data)  # type: ignore
    if req.is_valid():
        target: TargetVertex = get_object_or_404(
            TargetVertex, pk=req.data.get("target_id")
        )
        outline_time: OutlineTime = get_object_or_404(
            OutlineTime.objects.select_related("outline", "outline__owner"),
            pk=req.data.get("time_id"),
            outline__owner=request.user,
        )

        if target.outline_time is None:
            old_id = "none"
        else:
            old_id = f"{target.pk}-time-{target.outline_time.pk}"

        target.outline_time = outline_time
        target.save()

        return Response(
            {"new": f"{target.pk}-time-{req.data.get('time_id')}", "old": old_id},
            status=status.HTTP_200_OK,
        )

    return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(exclude=True)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_target(request: Request):
    """
    For given target id, delete obj.
    """
    req = TargetDeleteSerializer(data=request.data)  # type: ignore
    if req.is_valid():
        target: TargetVertex = get_object_or_404(
            TargetVertex.objects.select_related("outline"), pk=req.data.get("target_id")
        )
        get_object_or_404(Outline, owner=request.user, pk=target.outline.pk)
        with transaction.atomic():
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
    return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(exclude=True)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def overview_state_update(request: Request):
    req = OverwiewStateHideSerializer(data=request.data)  # type: ignore
    if req.is_valid():
        get_object_or_404(Outline, id=req.data.get("outline_id"), owner=request.user)
        overview: Overview = get_object_or_404(Overview, token=req.data.get("token"))

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
    return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(exclude=True)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_weight_model_buildings(request: Request):
    """
    For given weight model updates its building.
    """
    req = ChangeWeightBuildingSerializer(data=request.data)  # type: ignore
    if req.is_valid():
        get_object_or_404(Outline, pk=req.data.get("outline_id"), owner=request.user)
        weight: WeightModel = get_object_or_404(
            WeightModel, pk=req.data.get("weight_id")
        )
        weight.building = req.data.get("building")
        weight.save()
        weight.refresh_from_db()
        new_building: str = weight.get_building_display()  # type: ignore
        return Response({"name": new_building}, status=status.HTTP_200_OK)

    return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(exclude=True)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_buildings_array(request: Request):
    """
    For given outline updates array with buildings.
    """
    req = ChangeBuildingsArraySerializer(data=request.data)  # type: ignore
    if req.is_valid():
        outline: Outline = get_object_or_404(
            Outline, id=req.data.get("outline_id"), owner=request.user
        )
        outline.initial_outline_buildings = req.data["buildings"]
        outline.actions.form_building_order_change(outline)
        outline.save(update_fields=["initial_outline_buildings"])
        return Response(status=status.HTTP_200_OK)

    return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(exclude=True)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def reset_user_messages(request: Request):
    """
    For given user reset his notifications.
    """
    profile: Profile = get_object_or_404(Profile, user=request.user)
    profile.messages = 0
    profile.save()
    return Response(status=status.HTTP_200_OK)


@extend_schema(exclude=True)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stripe_config(request: Request):
    stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
    return Response(stripe_config, status=status.HTTP_200_OK)


@extend_schema(exclude=True)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def stripe_checkout_session(request: Request):  # pragma: no cover
    """Stripe checkout session endpoint"""
    import stripe

    req = StripeSessionAmount(data=request.data)  # type: ignore
    if req.is_valid():
        user_pk: str = str(request.user.pk)
        profile: Profile = Profile.objects.get(user_id=user_pk)
        try:
            price: StripePrice = StripePrice.objects.get(
                amount=req.data["amount"],
                active=True,
                product__active=True,
                currency=profile.get_currency,
            )

        except StripePrice.DoesNotExist:
            log.error(
                "stripe_checkout_session(), StripePrice not found:"
                f" curr:{profile.get_currency},amount:{req.data.get('amount')}"
            )
            metrics.ERRORS.labels("stripe_error").inc()
            return Response(
                {"error": "Could not found price for given user and amount."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        host = request.get_host()
        scheme = request.scheme
        success = reverse("base:payment_done")
        cancel = reverse("base:premium")
        try:
            language = translation.get_language()
            checkout_session = stripe.checkout.Session.create(
                success_url=f"{scheme}://{host}{success}",
                cancel_url=f"{scheme}://{host}{cancel}",
                client_reference_id=user_pk,
                customer_email=profile.user.email,
                metadata={"language": language},
                mode="payment",
                line_items=[
                    {
                        "quantity": 1,
                        "price": price.price_id,
                    }
                ],
                api_key=settings.STRIPE_SECRET_KEY,
                stripe_version=settings.STRIPE_VERSION,
            )
        except Exception as e:
            log.error(f"stripe_checkout_session() {e}")
            metrics.ERRORS.labels("stripe_error").inc()
            return Response(
                {"error": "unknown error when creating stripe checkout session"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:
            session_id = checkout_session["id"]
            return Response({"sessionId": session_id}, status=status.HTTP_200_OK)
    return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(exclude=True)
@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request: Request):  # pragma: no cover # noqa: PLR0911
    """Stripe webhooks endpoint to verify payment success"""
    import stripe

    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    if sig_header is None:
        log.error("stripe_webhook() sig_header is None")
        metrics.ERRORS.labels("stripe_error").inc()
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret,
            api_key=settings.STRIPE_SECRET_KEY,
        )
    except ValueError as err:
        # Invalid payload
        log.error(f"stripe_webhook() invalid payload {err}")
        metrics.ERRORS.labels("stripe_error").inc()
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.SignatureVerificationError as err:
        # Invalid signature
        log.error(f"stripe_webhook() invalid signature {err}")
        metrics.ERRORS.labels("stripe_error").inc()
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        log.error(f"stripe_webhook() unknown error {err}")
        metrics.ERRORS.labels("stripe_error").inc()
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        evt_id: str = event["id"]
        if not Payment.objects.filter(event_id=evt_id).exists():
            current_date: datetime.date = timezone.localdate()
            data: dict = event["data"]["object"]
            user: User = User.objects.get(pk=data["client_reference_id"])
            amount: int = int(data["amount_total"])
            currency: str = data["currency"].upper()
            language = data["metadata"]["language"]
            payment_intent = data["payment_intent"]
            try:
                price: StripePrice = StripePrice.objects.get(
                    currency=currency,
                    amount=amount,
                )
            except StripePrice.DoesNotExist:
                metrics.ERRORS.labels("stripe_error").inc()
                log.error(
                    "stripe_webhook() checkout.session.completed "
                    f"price does not exists: {amount} {currency}"
                )
                return Response(status=status.HTTP_400_BAD_REQUEST)

            Payment.objects.get_or_create(
                event_id=evt_id,
                defaults={
                    "user": user,
                    "amount": int(amount / 100),
                    "from_stripe": True,
                    "currency": currency,
                    "months": price.product.months,
                    "payment_intent_id": payment_intent,
                    "language": language,
                    "payment_date": current_date,
                },
            )
        return Response(status=status.HTTP_200_OK)

    if event["type"] in [
        "price.created",
        "price.deleted",
        "price.updated",
        "product.created",
        "product.deleted",
        "product.updated",
    ]:
        try:
            synchronize_stripe()
        except Exception as err:
            metrics.ERRORS.labels("stripe_error").inc()
            log.error(f"stripe_webhook() synchronize_stripe failed {err}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(exclude=True)
@api_view(["GET"])
@permission_classes([AllowAny, MetricsExportSecretPermission])
def metrics_export(request: Request):
    registry = prometheus_client.CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    metrics_page = prometheus_client.generate_latest(registry)
    return HttpResponse(
        metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST, status=200
    )


@extend_schema(exclude=True)
@api_view(["GET"])
@permission_classes([IsAdminUser])
def trigger_error(_: Request) -> HttpResponse:
    division_by_zero = 1 / 0  # type: ignore # noqa: F841

    return HttpResponse()


@extend_schema(
    tags=["overview"],
    description="Endpoint (anonymous) to get overview data by it's unique token, the same overview can be seen in graphical version using path: `https://plemiona-planer.pl/en/overview/{token}`",
    parameters=[
        OpenApiParameter(name="token", type=OpenApiTypes.STR),
        OpenApiParameter(name="language", type=OpenApiTypes.STR, enum=list(LANGUAGES)),
    ],
    responses={
        200: OpenApiResponse(
            response=serializers.OverviewSerializer, description="success"
        ),
        404: OpenApiResponse(
            response=serializers.ErrorDetailSerializer,
            description="there is no overview in database for provided token",
            examples=[
                OpenApiExample(
                    name="overview not found",
                    value={"detail": "No Overview matches the given query."},
                )
            ],
        ),
        429: OpenApiResponse(
            response=serializers.ErrorDetailSerializer,
            description=f"too many requests, limit is {settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon']} per IP",
            examples=[
                OpenApiExample(
                    name="too many requests",
                    value={
                        "detail": "Request was throttled. Expected available in 16 seconds."
                    },
                )
            ],
        ),
        500: OpenApiResponse(
            response=serializers.ErrorDetailSerializer,
            description="server error - report it",
            examples=[
                OpenApiExample(
                    name="inconsistent data",
                    value={
                        "detail": "Inconsistent data in database: {'outline': {'date': [ErrorDetail(string='This field is required.', code='required')]}}"
                    },
                )
            ],
        ),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def public_overview(request: Request) -> HttpResponse:
    token = request.query_params.get("token")
    language = request.query_params.get("language", "en")
    if language not in LANGUAGES:
        language = "en"

    activate(language)

    overview: models.Overview = get_object_or_404(
        models.Overview.objects.filter(pk=token).only(
            "outline_overview_id", "show_hidden", "player"
        ),
    )

    output = get_overview_data(
        overview.outline_overview_id,
        show_hidden=overview.show_hidden,
        player=overview.player,
        language=language,
        version=4,
    )

    if not output.is_valid():
        return Response(
            data={"detail": f"Inconsistent data in database: {output.errors}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        data=output.data,
        status=status.HTTP_200_OK,
    )


@extend_schema(exclude=True)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def shipment_overviews(request: Request, pk: int) -> HttpResponse:
    language = request.query_params.get("language", "en")
    if language not in LANGUAGES:
        language = "en"

    activate(language)

    shipment = get_object_or_404(
        Shipment.objects.prefetch_related(
            Prefetch(
                "overviews",
                queryset=Overview.objects.only("player", "outline_overview_id"),
            )
        ),
        pk=pk,
        owner=request.user,
    )
    overviews = list(shipment.overviews.all())

    if not overviews:
        return Response(
            data={"detail": "No overviews found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    outline_overviews = sorted(
        set([overview.outline_overview_id for overview in overviews])
    )

    output = get_overview_data_many(
        outline_overviews,
        show_hidden=False,
        player=overviews[0].player,
        language=language,
        version=4,
    )

    if not output.is_valid():
        return Response(
            data={"detail": f"Inconsistent data in database: {output.errors}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        data=output.data,
        status=status.HTTP_200_OK,
    )


@extend_schema(exclude=True)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def shipment_add_to_send_lst(request: Request, pk: int) -> HttpResponse:
    req = ShipmentUpdateSendListSerializer(data=request.data)  # type: ignore
    if req.is_valid():
        shipment = get_object_or_404(
            Shipment,
            pk=pk,
            owner=request.user,
        )
        if req.data["id"] not in shipment.sent_lst:
            shipment.sent_lst.append(req.data["id"])
            shipment.save(update_fields=["sent_lst"])
        return Response(status=status.HTTP_200_OK)

    return Response(req.errors, status=status.HTTP_400_BAD_REQUEST)
