from itertools import zip_longest

from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Max, Min

from base import models
from base import forms
from tribal_wars import basic


@login_required
def initial_add_first(request, id1, id2, id3):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
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
                basic.Village(target.target).distance(
                    basic.Village(weight.start)
                ),
                1,
            ),
            first_line=weight.first_line,
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


@login_required
def initial_add_first_fake(request, id1, id2, id3):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
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
        if weight.nobleman_left > 0:
            army = 0
            nobles = 1

        elif weight.off_left < 100:
            army = weight.off_left
            nobles = 0

        else:
            army = 100
            nobles = 0

        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            off=army,
            nobleman=nobles,
            order=order,
            distance=round(
                basic.Village(target.target).distance(
                    basic.Village(weight.start)
                ),
                1,
            ),
            first_line=weight.first_line,
        )
        weight.off_state += army
        weight.off_left -= army
        weight.nobleman_state += nobles
        weight.nobleman_left -= nobles
        weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


@login_required
def initial_add_last_fake(request, id1, id2, id3):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
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
        if weight.nobleman_left > 0:
            army = 0
            nobles = 1

        elif weight.off_left < 100:
            army = weight.off_left
            nobles = 0

        else:
            army = 100
            nobles = 0

        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            off=army,
            nobleman=nobles,
            order=order,
            distance=round(
                basic.Village(target.target).distance(
                    basic.Village(weight.start)
                ),
                1,
            ),
            first_line=weight.first_line,
        )
        weight.off_state += army
        weight.off_left -= army
        weight.nobleman_state += nobles
        weight.nobleman_left -= nobles
        weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


@login_required
def initial_add_last(request, id1, id2, id3):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
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
                basic.Village(target.target).distance(
                    basic.Village(weight.start)
                ),
                1,
            ),
            first_line=weight.first_line,
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

@login_required
def initial_hide_weight(request, id1, id2, id3):
    if request.method == "POST":
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight = get_object_or_404(models.WeightMaximum, pk=id3)
        weight.hidden = not weight.hidden
        weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()

@login_required
def initial_move_down(request, id1, id2, id4):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.get(pk=id4)
        target = get_object_or_404(models.TargetVertex, pk=id2)
        order1 = weight_model.order

        next_weight = (
            models.WeightModel.objects.filter(order__gt=order1)
            .filter(target=target)
            .order_by("order")
            .first()
        )

        if next_weight is not None:
            weight_model.order = next_weight.order
            weight_model.save()
            next_weight.order = order1
            next_weight.save()
        request.session["weight"] = weight_model.id
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


@login_required
def initial_move_up(request, id1, id2, id4):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.get(pk=id4)
        target = get_object_or_404(models.TargetVertex, pk=id2)
        order1 = weight_model.order

        next_weight = (
            models.WeightModel.objects.filter(order__lt=order1)
            .filter(target=target)
            .order_by("-order")
            .first()
        )

        if next_weight is not None:
            weight_model.order = next_weight.order
            weight_model.save()
            next_weight.order = order1
            next_weight.save()
        request.session["weight"] = weight_model.id
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


@login_required
def initial_weight_delete(request, id1, id2, id4):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.select_related(
            "state"
        ).filter(pk=id4)[0]
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


@login_required
def initial_divide(request, id1, id2, id4, n):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight = models.WeightModel.objects.select_related("state").filter(
            pk=id4
        )[0]
        n_list = [i + 1 for i in range(n - 1)]
        nob_list = [i for i in range(max(weight.nobleman - 1, 0))]
        if n > weight.nobleman:
            zipped_list = zip_longest(n_list, nob_list)
            nob_number = max(weight.nobleman - 1, 0)
        else:
            zipped_list = zip(n_list, nob_list)
            nob_number = n - 1

        off = weight.off // n
        rest = weight.off - off * n
        update_list = []
        create_list = []
        for number, nob in zipped_list:
            if nob is None:
                nob = 0
            else:
                nob = 1

            create_list.append(
                models.WeightModel(
                    target=weight.target,
                    player=weight.player,
                    start=weight.start,
                    state=weight.state,
                    off=off,
                    nobleman=nob,
                    order=weight.order + number,
                    distance=weight.distance,
                    first_line=weight.first_line,
                )
            )
        weight.off = off + rest
        weight.nobleman = weight.nobleman - nob_number
        weight.save()

        for next_weight in models.WeightModel.objects.filter(
            target=weight.target, order__gt=weight.order
        ):
            next_weight.order = next_weight.order + n
            update_list.append(next_weight)

        models.WeightModel.objects.bulk_create(create_list)
        models.WeightModel.objects.bulk_update(update_list, ["order"])

        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


@login_required
def overview_hide_unhide(request, id1, token):

    instance = get_object_or_404(models.Outline, id=id1, owner=request.user)
    overview = get_object_or_404(
        models.Overview, token=token, outline=instance
    )

    new_state = not bool(overview.show_hidden)
    overview.show_hidden = new_state

    overview.save()
    return redirect("base:planer_detail_results", id1)


@login_required
def delete_target(request, id1, id2):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        page = request.GET.get("page")
        mode = request.GET.get("mode")

        target = models.TargetVertex.objects.get(pk=id2)
        weights = models.WeightModel.objects.select_related("state").filter(
            target=target
        )
        # deletes weights related to this target and updates weight state
        for weight_model in weights:
            weight_model.state.off_left += weight_model.off
            weight_model.state.off_state -= weight_model.off
            weight_model.state.nobleman_left += weight_model.nobleman
            weight_model.state.nobleman_state -= weight_model.nobleman
            weight_model.state.save()
            weight_model.delete()

        target.delete()
        return redirect(
            reverse("base:planer_initial", args=[id1])
            + f"?page={page}&mode={mode}"
        )

    return Http404()


@login_required
def change_weight_off(request, id1, id2):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        page = request.GET.get("page")
        mode = request.GET.get("mode")
        player = request.GET.get("player")

        weight_max = get_object_or_404(models.WeightMaximum, pk=id2)
        form = forms.ChangeWeightMaxOff(request.POST)
        if form.is_valid():
            off = request.POST.get("off")
            noble = request.POST.get("noble")
            weight_max.off_max = off
            weight_max.left = off
            weight_max.nobleman_max = noble
            weight_max.nobleman_left = noble
            weight_max.save()

        return redirect(
            reverse("base:planer_initial", args=[id1])
            + f"?page={page}&mode={mode}&player={player}"
        )
