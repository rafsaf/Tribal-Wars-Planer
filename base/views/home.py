from django.shortcuts import render, redirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from markdownx.utils import markdownify
from tribal_wars.database_update import cron_schedule_data_update
from base import models
from tribal_wars import basic

def database_update(request):
    # ZMIENIC
    """ to update database manually, superuser required """
    if request.user.is_superuser:
        cron_schedule_data_update()
        return redirect("base:base")
    else:
        return Http404()


def base_view(request):
    """ base view """
    return render(request, "base/base.html")


def base_documentation(request):
    """ base documentation view"""
    doc = models.Documentation.objects.get(title="Doc").main_page
    doc = markdownify(doc)

    context = {"doc": doc}
    return render(request, "base/documentation.html", context)

def overview(request, token):
    """ Safe url for member of tribe """
    try:
        overview = models.Overview.objects.select_related('outline').get(pk=token)
    except models.Overview.DoesNotExist:
        return redirect('base:overview_fail')

    own_weight_target = set()
    each_weight_target = set()

    own_weights = models.WeightModel.objects.select_related('target').filter(
        target__outline__id=overview.outline.id, player=overview.player).order_by('order')
    
    for weight in own_weights:
        if weight.target in each_weight_target:
            continue

        if weight.nobleman > 0 and weight.distance < 14: # < 8h
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
        models.WeightModel.objects.select_related("target")
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
    query = target_context.items()
    print(query)
    context = {'query': query, 'overview': overview}
    return render(request, 'base/overview.html', context=context)

def overview_fail(request):
    """ Redirected from overview with fail token """
    return render(request, 'base/overview_fail.html')