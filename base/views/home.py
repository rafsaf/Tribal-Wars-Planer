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
from datetime import date
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import get_language
from markdownx.utils import markdownify

from base import models
from base.models import PDFPaymentSummary
from utils.basic.pdf import generate_pdf_summary


def base_view(request):
    """base view"""
    stats = {}
    INITIAL_DATE = date(year=2020, month=9, day=1)
    days: int = (timezone.localdate() - INITIAL_DATE).days
    stats["days"] = days
    try:
        users: Optional[int] = User.objects.latest("pk").pk
    except User.DoesNotExist:
        users = 0

    stats["users"] = users

    try:
        outlines: int = models.Outline.objects.latest("pk").pk
    except models.Outline.DoesNotExist:
        outlines = 0

    stats["outlines"] = outlines

    try:
        targets: int = models.TargetVertex.objects.latest("pk").pk
    except models.TargetVertex.DoesNotExist:
        targets = 0

    stats["targets"] = targets

    try:
        orders: int = models.WeightModel.objects.latest("pk").pk
    except models.WeightModel.DoesNotExist:
        orders = 0

    stats["orders"] = orders

    context = {"stats": stats}
    return render(request, "base/base.html", context)


def base_documentation(request):
    """base documentation view"""
    language_code = get_language()

    doc = models.Documentation.objects.get_or_create(
        title="documentation", language=language_code, defaults={"main_page": ""}
    )[0].main_page
    doc = markdownify(doc)

    context = {"doc": doc}
    return render(request, "base/documentation.html", context)


def overview_view(request, token):
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

    context = {"query": query, "overview": overview}
    return render(request, "base/overview.html", context=context)


@login_required
def payment_sum_up_view(request: HttpRequest) -> HttpResponse:
    user: User = request.user  # type: ignore
    if user.is_superuser and user.username == "admin":
        if request.method == "POST" and "form" in request.POST:
            generate_pdf_summary()
            return redirect("base:payment_summary")
        summary = PDFPaymentSummary.objects.all()
        context = {"summary": summary}
        return render(request, "base/user/payments_summary.html", context=context)
    else:
        raise Http404()
