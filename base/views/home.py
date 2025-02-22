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


import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation

from base import models
from base.models import PDFPaymentSummary
from utils.basic import is_android_tw_app_webview
from utils.basic.pdf import generate_pdf_summary

log = logging.getLogger(__name__)


def base_view(request) -> HttpResponse:
    stats = {
        "users": User.objects.aggregate(latest_pk=Coalesce(Max("pk"), 0))["latest_pk"],
        "outlines": models.Outline.objects.aggregate(latest_pk=Coalesce(Max("pk"), 0))[
            "latest_pk"
        ],
        "targets": models.TargetVertex.objects.aggregate(
            latest_pk=Coalesce(Max("pk"), 0)
        )["latest_pk"],
        "orders": models.WeightModel.objects.aggregate(
            latest_pk=Coalesce(Max("pk"), 0)
        )["latest_pk"],
    }

    context = {
        "stats": stats,
        "registration_open": settings.REGISTRATION_OPEN,
    }

    return render(request, "base/base.html", context)


def base_documentation(request: HttpRequest):
    """base documentation view"""
    language = translation.get_language()
    if request.path.startswith(language):
        return HttpResponseRedirect(language + request.path.removesuffix("/") + "/")
    raise Http404()


def overview_view(request: HttpRequest, token: str):
    """Safe url for member of tribe"""
    overview: models.Overview = get_object_or_404(
        models.Overview.objects.select_related().filter(pk=token)
    )
    outline_overview: models.OutlineOverview = overview.outline_overview
    if overview.outline is not None:
        outline: models.Outline = overview.outline
        outline.actions.visit_overview_visited(outline)

    query = []
    targets = json.loads(outline_overview.targets_json)
    weights = json.loads(outline_overview.weights_json)
    if overview.show_hidden:
        for target, lst in weights.items():
            for weight in lst:
                if weight["player"] == overview.player:
                    query.append((targets[target], lst))
                    break

    else:
        for target, lst in weights.items():
            owns = [weight for weight in lst if weight["player"] == overview.player]
            if len(owns) > 0:
                alls = False
                for weight in owns:
                    if weight["nobleman"] > 0 and weight["distance"] < 14:
                        alls = True
                        break
                if alls:
                    query.append((targets[target], lst))
                else:
                    query.append((targets[target], owns))

    context = {
        "query": query,
        "overview": overview,
        "android_tw_app_webview": is_android_tw_app_webview(request=request),
    }
    return render(request, "base/overview.html", context=context)


@login_required
def payment_sum_up_view(request: HttpRequest) -> HttpResponse:
    user: User = request.user  # type: ignore
    if user.is_superuser and user.username == "admin":
        if request.method == "POST" and "form" in request.POST:
            generate_pdf_summary(request=request)
            return redirect("base:payment_summary")
        summary_periods = (
            PDFPaymentSummary.objects.all()
            .order_by("period")
            .distinct("period")
            .values_list("period", flat=True)
        )
        summary = []
        for period in summary_periods:
            summary.append(
                PDFPaymentSummary.objects.filter(period=period).latest("created_at")
            )
        context = {"summary": summary}
        return render(request, "base/user/payments_summary.html", context=context)
    else:
        raise Http404()
