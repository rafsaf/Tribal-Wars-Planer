

from django.shortcuts import render, redirect
from django.db.models import Max, Min
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
import trbial_wars.outline_initial as initial
import trbial_wars.basic as basic
from base import models, forms


@login_required
def initial_planer(request, _id):
    """ view with form for initial period outline """

    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)

    if instance.off_troops == "":
        request.session["error"] = "Zbiórka Wojsko pusta!"
        return redirect("base:planer_detail", _id)

    if "form1" in request.POST:
        request.session["is_allowed"] = "ok"
        return redirect("base:planer_initial_form", _id)

    target_query = models.TargetVertex.objects.filter(outline=instance)
    target_context = {}
    for target in target_query:
        target_context[target] = list()

    for weight in models.WeightModel.objects.select_related('target').filter(target__in=target_query).order_by('order'):
        weight.distance = round(basic.Village(weight.start, validate=False).distance(
            basic.Village(weight.target.target, validate=False)
        ), 1)
        weight.off = f'{round(weight.off / 1000,1)}k'
        target_context[weight.target].append(weight)

    target_context = list(target_context.items())
    paginator = Paginator(target_context, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"instance": instance, "query": page_obj}
    return render(request, "base/new_outline/new_outline_initial_period2.html", context)


@login_required
def initial_form(request, _id):
    """ view with table with created outline, returned after valid filled form earlier """

    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)

    if instance.off_troops == "":
        request.session["error"] = "Zbiórka Wojsko pusta!"
        return redirect("base:planer_detail", _id)

    is_allowed = request.session.get("is_allowed")
    # always go to the next view after form confirmation OR if user want to
    if is_allowed is None and instance.initial_outline_targets != "":
        return redirect("base:planer_initial", _id)

    form1 = forms.InitialOutlineForm(request.POST or None, world=instance.world)
    form1.fields["target"].initial = instance.initial_outline_targets

    if "form1" in request.POST:
        if form1.is_valid():
            target = request.POST.get("target")
            instance.initial_outline_targets = target
            instance.save()
            # make outline
            try:
                initial.make_outline(instance)
            except EnvironmentError:
                request.session[
                    "error"
                ] = "Wygląda na to, że Twoja Zbiórka Wojska nie jest już aktualna! Aby skorzystać z planera: skopiuj dane z podglądu i popraw błędy lub wklej aktualne dane o wojsku \n"
                return redirect("base:planer_detail", _id)

            try:
                del request.session["is_allowed"]
            except KeyError:
                pass
            return redirect("base:planer_initial", _id)

    context = {"instance": instance, "form1": form1}
    return render(request, "base/new_outline/new_outline_initial_period1.html", context)



@login_required
def initial_target(request, id1, id2):
    """ view with form for initial period outline detail """

    instance = get_object_or_404(models.Outline, id=id1, owner=request.user)
    target = get_object_or_404(models.TargetVertex, pk=id2)

    if instance.off_troops == "":
        request.session["error"] = "Zbiórka Wojsko pusta!"
        return redirect("base:planer_detail", id1)

    nonused_vertices = models.WeightMaximum.objects.filter(outline=instance)

    result_lst = models.WeightModel.objects.filter(target=target).order_by("order")
    for weight in result_lst:
        weight.distance = round(weight.distance, 1)
    ## sort
    sort = request.GET.get("sort")
    village = basic.Village(target.target)
    if sort is None:
        sort = "-off_left"
    if sort == "distance":
        nonused_vertices = list(nonused_vertices)
        for weight in nonused_vertices:
            weight.distance = round(basic.Village(weight.start).distance(village),1)
        nonused_vertices.sort(
            key=lambda weight: weight.distance
        )
        paginator = Paginator(nonused_vertices, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    elif sort == "-distance":
        nonused_vertices = list(nonused_vertices)
        for weight in nonused_vertices:
            weight.distance =  round(basic.Village(weight.start).distance(village),1)
        nonused_vertices.sort(
            key=lambda weight: weight.distance, reverse=True
        )
        paginator = Paginator(nonused_vertices, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        if sort in {'-off_left', '-nobleman_left'}:
            nonused_vertices = nonused_vertices.order_by(sort)
        else:
            nonused_vertices = nonused_vertices.order_by('-off_left')
        paginator = Paginator(nonused_vertices, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        for weight in page_obj:
            weight.distance =  round(basic.Village(weight.start).distance(village),1)

    form = forms.WeightForm()

    context = {
        "instance": instance,
        "target": target,
        "result_lst": result_lst,
        "form": form,
        "page_obj": page_obj,
        "sort": sort,
    }
    return render(request, "base/new_outline/new_outline_initial_period3.html", context)


@csrf_protect
def initial_add_first(request, id1, id2, id3):
    if request.method == "POST":
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        target = get_object_or_404(models.TargetVertex, pk=id2)
        weight = get_object_or_404(models.WeightMaximum, pk=id3)
        if not models.WeightModel.objects.filter(target=target).exists():
            order = 0
        else:
            order = (
                models.WeightModel.objects.filter(target=target).aggregate(
                    Min("order")
                )["order__min"]
                - 1
            )
        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            off=weight.off_left,
            nobleman=weight.nobleman_left,
            order=order,
            distance=round(
                basic.Village(target.target).distance(basic.Village(weight.start)), 1
            ),
        )
        weight.off_state += weight.off_left
        weight.off_left = 0
        weight.nobleman_state += weight.nobleman_left
        weight.nobleman_left = 0
        weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


def initial_add_last(request, id1, id2, id3):
    if request.method == "POST":
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        target = get_object_or_404(models.TargetVertex, pk=id2)
        weight = get_object_or_404(models.WeightMaximum, pk=id3)
        if not models.WeightModel.objects.filter(target=target).exists():
            order = 0
        else:
            order = (
                models.WeightModel.objects.filter(target=target).aggregate(
                    Max("order")
                )["order__max"]
                + 1
            )
        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            off=weight.off_left,
            nobleman=weight.nobleman_left,
            order=order,
            distance=round(
                basic.Village(target.target).distance(basic.Village(weight.start)), 1
            ),
        )
        weight.off_state += weight.off_left
        weight.off_left = 0
        weight.nobleman_state += weight.nobleman_left
        weight.nobleman_left = 0
        weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


def initial_move_down(request, id1, id2, id4):
    if request.method == "POST":
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.get(pk=id4)
        target = get_object_or_404(models.TargetVertex, pk=id2)
        order1 = weight_model.order

        next_weight = (
            models.WeightModel.objects.filter(order__gt=order1).filter(target=target)
            .order_by("order")
            .first()
        )

        if next_weight is not None:
            weight_model.order = next_weight.order
            weight_model.save()
            next_weight.order = order1
            next_weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


def initial_move_up(request, id1, id2, id4):
    if request.method == "POST":
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.get(pk=id4)
        target = get_object_or_404(models.TargetVertex, pk=id2)
        order1 = weight_model.order

        next_weight = (
            models.WeightModel.objects.filter(order__lt=order1).filter(target=target)
            .order_by("-order")
            .first()
        )
        if next_weight is not None:
            weight_model.order = next_weight.order
            weight_model.save()
            next_weight.order = order1
            next_weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


def initial_weight_delete(request, id1, id2, id4):
    if request.method == "POST":
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.select_related("state").filter(
            pk=id4
        )[0]
        weight_model.state.off_left += weight_model.off
        weight_model.state.off_state -= weight_model.off
        weight_model.state.nobleman_left += weight_model.nobleman
        weight_model.state.nobleman_state -= weight_model.nobleman
        weight_model.state.save()
        weight_model.delete()

        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()

