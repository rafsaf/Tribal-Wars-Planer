import json

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from markdownx.utils import markdownify


from base import models
from tribal_wars import basic


def base_view(request):
    """ base view """
    return render(request, "base/base.html")


def base_documentation(request):
    """ base documentation view"""
    language_code = get_language()

    doc = models.Documentation.objects.get_or_create(
        title="documentation", language=language_code, defaults={"main_page": ""}
    )[0].main_page
    doc = markdownify(doc)

    context = {"doc": doc}
    return render(request, "base/documentation.html", context)


def overview_view(request, token):
    """ Safe url for member of tribe """
    overview = get_object_or_404(
        models.Overview.objects.select_related().filter(pk=token)
    )
    outline_overview = overview.outline_overview

    if outline_overview.targets_json != "":
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

    else:
        own_weight_target = set()
        each_weight_target = set()

        own_weights = (
            models.WeightModelOverview.objects.select_related()
            .filter(target__outline_overview=outline_overview, player=overview.player)
            .order_by("order")
        )

        for weight in own_weights:
            if weight.target in each_weight_target:
                continue

            if overview.show_hidden:
                each_weight_target.add(weight.target)
                own_weight_target.discard(weight.target)

            elif weight.nobleman > 0 and weight.distance < 14:  # < 8h
                each_weight_target.add(weight.target)
                own_weight_target.discard(weight.target)
            else:
                own_weight_target.add(weight.target)

        target_context = {}

        for target in own_weight_target:
            target_context[target] = list()
        for weight in own_weights:
            if weight.target in own_weight_target:
                weight.distance = round(
                    basic.Village(weight.start, validate=False).distance(
                        basic.Village(weight.target.target, validate=False)
                    ),
                    1,
                )
                weight.off = f"{round(weight.off / 1000,1)}k"
                target_context[weight.target].append(weight)

        for target in each_weight_target:
            target_context[target] = list()
        for weight in (
            models.WeightModelOverview.objects.select_related()
            .filter(target__in=each_weight_target)
            .order_by("order")
        ):
            weight.distance = round(
                basic.Village(weight.start, validate=False).distance(
                    basic.Village(weight.target.target, validate=False)
                ),
                1,
            )
            weight.off = f"{round(weight.off / 1000,1)}k"
            target_context[weight.target].append(weight)
        query = list(target_context.items())
        query.sort(key=lambda tup: tup[0].fake)

    context = {"query": query, "overview": overview}
    return render(request, "base/overview.html", context=context)


def overview_fail(request):
    """ Redirected from overview with fail token """
    return render(request, "base/overview_fail.html")
