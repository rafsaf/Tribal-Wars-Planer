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
from django.forms.utils import ErrorList
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import translation

from base.models.overview import Overview
from rest_api.overview_data import get_overview_data

from .forms import ShipmentCreateForm, ShipmentOverviewTokenFormSet
from .models import Shipment

log = logging.getLogger(__name__)


@login_required
def my_shipments(request: HttpRequest) -> HttpResponse:
    shipments = Shipment.objects.filter(owner=request.user)
    context = {"shipments": shipments}

    return render(request, "orders/my_shipments.html", context)


@login_required
def shipment(request: HttpRequest, pk: int) -> HttpResponse:
    shipment = get_object_or_404(
        Shipment,
        pk=pk,
        owner=request.user,
    )

    context = {"shipment": shipment}

    return render(request, "orders/shipment.html", context)


@login_required
def add_shipment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
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
                if data["world"]["id"] != world_id or data["outline"]["date"] != date:
                    formset._non_form_errors = ErrorList(  # type: ignore
                        ["All overviews must belong to the same world and date."]
                    )
                    context = {
                        "form": form,
                        "formset": formset,
                    }
                    return render(request, "orders/add_shipment.html", context)

            # Create Shipment
            shipment = Shipment.objects.create(
                name=name,
                owner=request.user,
                date=date,
                world_id=world_id,
            )
            shipment.overviews.add(*overviews)
            # Redirect or show success (here, redirect to my_shipments)
            return redirect(reverse("shipments:my_shipments"))
        else:
            # Invalid form/formset
            context = {
                "form": form,
                "formset": formset,
            }
            return render(request, "orders/add_shipment.html", context)
    else:
        form = ShipmentCreateForm()
        formset = ShipmentOverviewTokenFormSet()
        context = {
            "form": form,
            "formset": formset,
        }
        return render(request, "orders/add_shipment.html", context)
