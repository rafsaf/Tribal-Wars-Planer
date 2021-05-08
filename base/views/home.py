from datetime import date
import json
from typing import Optional

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from markdownx.utils import markdownify
from django.utils import timezone
from django.contrib.auth.models import User

from base import models


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
    overview = get_object_or_404(
        models.Overview.objects.select_related().filter(pk=token)
    )
    outline_overview = overview.outline_overview

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


def overview_fail(request):
    """Redirected from overview with fail token"""
    return render(request, "base/overview_fail.html")
