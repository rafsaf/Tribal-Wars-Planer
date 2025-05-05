# Copyright 2025 Rafał Safin (rafsaf). All Rights Reserved.
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


import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.forms.utils import ErrorList
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy
from django.views.decorators.http import require_POST

from base.models.overview import Overview
from base.views.outline import get_show_hidden
from rest_api.overview_data import get_overview_data

from .forms import ShipmentCreateForm, ShipmentOverviewTokenFormSet
from .models import Shipment

log = logging.getLogger(__name__)


@login_required
def my_shipments(request: HttpRequest) -> HttpResponse:
    show_hidden = get_show_hidden(request)
    shipments = (
        Shipment.objects.filter(owner=request.user)
        .prefetch_related(
            Prefetch(
                "overviews",
                queryset=Overview.objects.defer(
                    "outline_overview",
                    "outline",
                    "table",
                    "string",
                    "extended",
                    "new_extended",
                    "deputy",
                    "player",
                    "show_hidden",
                    "removed",
                ).order_by("-created"),
            )
        )
        .select_related("world")
        .order_by("-created_at")
    )

    if not show_hidden:
        shipments = shipments.filter(hidden=False)

    context = {"shipments": shipments, "show_hidden": show_hidden}

    return render(request, "my_shipments.html", context)


@login_required
def shipment_send(request: HttpRequest, pk: int) -> HttpResponse:
    shipment = get_object_or_404(
        Shipment,
        pk=pk,
        owner=request.user,
    )

    context = {"shipment": shipment}

    return render(request, "shipment.html", context)


@login_required
def add_edit_shipment(request: HttpRequest, pk: int | None = None) -> HttpResponse:  # noqa: PLR0911
    if request.method == "POST":
        if pk is not None:
            shipment = get_object_or_404(
                Shipment,
                pk=pk,
                owner=request.user,
            )
            form = ShipmentCreateForm({"name": shipment.name})
            form.fields["name"].widget.attrs["readonly"] = True
        else:
            shipment = None
            form = ShipmentCreateForm(request.POST)

        formset = ShipmentOverviewTokenFormSet(request.POST)  # type: ignore

        if form.is_valid() and formset.is_valid():
            name = form.cleaned_data["name"]
            tokens = [
                f.cleaned_data["token"]
                for f in formset.forms
                if f.cleaned_data.get("token")
            ]
            overviews = list(
                Overview.objects.filter(token__in=tokens).select_related(
                    "outline_overview"
                )
            )

            # Get world and date from the first overview
            first_ov = overviews[0]
            serializer = get_overview_data(
                first_ov.outline_overview_id,
                show_hidden=first_ov.show_hidden,
                player=first_ov.player,
                language=translation.get_language(),
                version=1,
            )
            serializer.is_valid()
            data = serializer.data
            world_id = data["world"]["id"]
            date = data["outline"]["date"]
            player_name = first_ov.player
            # Check all overviews have the same world and date
            for overview in overviews:
                serializer = get_overview_data(
                    overview.outline_overview_id,
                    show_hidden=overview.show_hidden,
                    player=overview.player,
                    language=translation.get_language(),
                    version=1,
                )
                serializer.is_valid()
                data = serializer.data
                if data["world"]["id"] != world_id:
                    formset._non_form_errors = ErrorList(  # type: ignore
                        [gettext_lazy("All overviews must belong to the same world.")]
                    )
                    context = {
                        "form": form,
                        "formset": formset,
                        "shipment": shipment,
                    }
                    if shipment is not None:
                        return render(request, "edit_shipment.html", context)
                    return render(request, "add_shipment.html", context)
                player = overview.player
                if player != player_name:
                    formset._non_form_errors = ErrorList(  # type: ignore
                        [
                            gettext_lazy("All overviews must be for the same player."),
                            player,
                            gettext_lazy("does not match"),
                            player_name,
                        ]
                    )
                    context = {
                        "form": form,
                        "formset": formset,
                        "shipment": shipment,
                    }
                    if shipment is not None:
                        return render(request, "edit_shipment.html", context)
                    return render(request, "add_shipment.html", context)
            if shipment is None:
                # Create Shipment
                shipment = Shipment.objects.create(
                    name=name,
                    owner=request.user,
                    date=date,
                    world_id=world_id,
                )
                shipment.overviews.add(*overviews)
                # Redirect or show success (here, redirect to my_shipments)
                return redirect("shipments:my_shipments")
            else:
                shipment.overviews.clear()
                shipment.overviews.add(*overviews)
                return redirect("shipments:edit_shipment", pk)

        else:
            # Invalid form/formset
            if pk is not None:
                context = {
                    "form": form,
                    "formset": formset,
                    "shipment": shipment,
                }
                return render(request, "edit_shipment.html", context)
            context = {
                "form": form,
                "formset": formset,
            }
            return render(request, "add_shipment.html", context)
    else:
        if pk is not None:
            shipment = get_object_or_404(
                Shipment,
                pk=pk,
                owner=request.user,
            )
            form = ShipmentCreateForm(initial={"name": shipment.name})
            form.fields["name"].widget.attrs["readonly"] = True

            initial_data = [
                {"token": overview.token} for overview in shipment.overviews.all()
            ]
            formset = ShipmentOverviewTokenFormSet(initial=initial_data)  # type: ignore

            context = {
                "form": form,
                "formset": formset,
                "shipment": shipment,
            }

            return render(request, "edit_shipment.html", context)

        form = ShipmentCreateForm()
        formset = ShipmentOverviewTokenFormSet()

        context = {
            "form": form,
            "formset": formset,
        }
        return render(request, "add_shipment.html", context)


@login_required
@require_POST
def shipment_hide(request: HttpRequest, pk: int) -> HttpResponse:
    shipment = get_object_or_404(
        Shipment.objects.only("pk", "hidden"), id=pk, owner=request.user
    )
    show_hidden = get_show_hidden(request)

    if shipment.hidden:
        shipment.hidden = False
        shipment.save(update_fields=["hidden"])
    else:
        shipment.hidden = True
        shipment.save(update_fields=["hidden"])

    return redirect(
        reverse("shipments:my_shipments") + f"?show-hidden={str(show_hidden).lower()}"
    )


@login_required
@require_POST
def shipment_delete(request: HttpRequest, pk: int) -> HttpResponse:
    shipment = get_object_or_404(Shipment.objects.only("pk"), id=pk, owner=request.user)
    show_hidden = get_show_hidden(request)

    shipment.delete()
    return redirect(
        reverse("shipments:my_shipments") + f"?show-hidden={str(show_hidden).lower()}"
    )
