from itertools import zip_longest

from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from base import models
from utils import basic


@require_POST
@login_required
def initial_add_first(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Min("order"))[
                "order__min"
            ]
            - 1
        )
    models.WeightModel.objects.create(
        target=target,
        player=weight.player,
        start=weight.start,
        state=weight,
        off=weight.off_left,
        catapult=weight.catapult_left,
        nobleman=weight.nobleman_left,
        order=order,
        distance=round(
            basic.Village(target.target).distance(basic.Village(weight.start)),
            1,
        ),
        first_line=weight.first_line,
    )
    weight.off_state += weight.off_left
    weight.off_left = 0
    weight.nobleman_state += weight.nobleman_left
    weight.nobleman_left = 0
    weight.catapult_state += weight.catapult_left
    weight.catapult_left = 0
    weight.save()
    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_first_off(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Min("order"))[
                "order__min"
            ]
            - 1
        )
    models.WeightModel.objects.create(
        target=target,
        player=weight.player,
        start=weight.start,
        state=weight,
        off=weight.off_left,
        catapult=weight.catapult_left,
        nobleman=0,
        order=order,
        distance=round(
            basic.Village(target.target).distance(basic.Village(weight.start)),
            1,
        ),
        first_line=weight.first_line,
    )
    weight.off_state += weight.off_left
    weight.off_left = 0
    weight.catapult_state += weight.catapult_left
    weight.catapult_left = 0
    weight.save()
    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_first_ruin(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Min("order"))[
                "order__min"
            ]
            - 1
        )
    if weight.catapult_left > 0:
        if weight.catapult_left > outline.initial_outline_catapult_default:
            catapult = outline.initial_outline_catapult_default
        else:
            catapult = weight.catapult_left

        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            off=catapult * 8,
            ruin=True,
            catapult=catapult,
            nobleman=0,
            order=order,
            distance=round(
                basic.Village(target.target).distance(basic.Village(weight.start)),
                1,
            ),
            first_line=weight.first_line,
        )
        weight.off_state += catapult * 8
        weight.off_left -= catapult * 8
        weight.catapult_state += catapult
        weight.catapult_left = weight.catapult_left - catapult
        weight.save()
    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_first_fake(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Min("order"))[
                "order__min"
            ]
            - 1
        )

    off_catapults = weight.catapult_left * 8
    off_else = weight.off_left - off_catapults

    if off_else >= 100:
        army = 100
        nobles = 0
        catapult = 0
    else:
        off_to_fill_out = 100 - off_else
        if off_catapults < off_to_fill_out:
            army = off_else + off_catapults
            nobles = 0
            catapult = weight.catapult_left
        else:
            catapult = off_to_fill_out // 8
            nobles = 0
            army = 8 * catapult + off_else

    models.WeightModel.objects.create(
        target=target,
        player=weight.player,
        start=weight.start,
        state=weight,
        catapult=catapult,
        off=army,
        nobleman=nobles,
        order=order,
        distance=round(
            basic.Village(target.target).distance(basic.Village(weight.start)),
            1,
        ),
        first_line=weight.first_line,
    )
    weight.off_state += army
    weight.off_left -= army
    weight.catapult_state += catapult
    weight.catapult_left -= catapult
    weight.nobleman_state += nobles
    weight.nobleman_left -= nobles
    weight.save()
    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_first_fake_noble(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Min("order"))[
                "order__min"
            ]
            - 1
        )
    if weight.nobleman_left > 0:
        army = 0
        nobles = 1
        catapult = 0

        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            catapult=catapult,
            off=army,
            nobleman=nobles,
            order=order,
            distance=round(
                basic.Village(target.target).distance(basic.Village(weight.start)),
                1,
            ),
            first_line=weight.first_line,
        )
        weight.nobleman_state += nobles
        weight.nobleman_left -= nobles
        weight.save()

    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_last_fake(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Max("order"))[
                "order__max"
            ]
            + 1
        )

    off_catapults = weight.catapult_left * 8
    off_else = weight.off_left - off_catapults

    if off_else >= 100:
        army = 100
        nobles = 0
        catapult = 0
    else:
        off_to_fill_out = 100 - off_else
        if off_catapults < off_to_fill_out:
            army = off_else + off_catapults
            nobles = 0
            catapult = weight.catapult_left
        else:
            catapult = off_to_fill_out // 8
            nobles = 0
            army = 8 * catapult + off_else

    models.WeightModel.objects.create(
        target=target,
        player=weight.player,
        start=weight.start,
        state=weight,
        catapult=catapult,
        off=army,
        nobleman=nobles,
        order=order,
        distance=round(
            basic.Village(target.target).distance(basic.Village(weight.start)),
            1,
        ),
        first_line=weight.first_line,
    )
    weight.off_state += army
    weight.off_left -= army
    weight.catapult_state += catapult
    weight.catapult_left -= catapult
    weight.nobleman_state += nobles
    weight.nobleman_left -= nobles
    weight.save()
    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_last_fake_noble(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Max("order"))[
                "order__max"
            ]
            + 1
        )
    if weight.nobleman_left > 0:
        army = 0
        nobles = 1
        catapult = 0

        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            catapult=catapult,
            off=army,
            nobleman=nobles,
            order=order,
            distance=round(
                basic.Village(target.target).distance(basic.Village(weight.start)),
                1,
            ),
            first_line=weight.first_line,
        )
        weight.nobleman_state += nobles
        weight.nobleman_left -= nobles
        weight.save()

    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_last_ruin(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Max("order"))[
                "order__max"
            ]
            + 1
        )
    if weight.catapult_left > 0:
        if weight.catapult_left > outline.initial_outline_catapult_default:
            catapult = outline.initial_outline_catapult_default
        else:
            catapult = weight.catapult_left

        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            off=catapult * 8,
            ruin=True,
            catapult=catapult,
            nobleman=0,
            order=order,
            distance=round(
                basic.Village(target.target).distance(basic.Village(weight.start)),
                1,
            ),
            first_line=weight.first_line,
        )
        weight.off_state += catapult * 8
        weight.off_left -= catapult * 8
        weight.catapult_state += catapult
        weight.catapult_left = weight.catapult_left - catapult
        weight.save()

    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_last_off(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Max("order"))[
                "order__max"
            ]
            + 1
        )
    models.WeightModel.objects.create(
        target=target,
        player=weight.player,
        start=weight.start,
        state=weight,
        off=weight.off_left,
        catapult=weight.catapult_left,
        nobleman=0,
        order=order,
        distance=round(
            basic.Village(target.target).distance(basic.Village(weight.start)),
            1,
        ),
        first_line=weight.first_line,
    )
    weight.off_state += weight.off_left
    weight.off_left = 0
    weight.catapult_state += weight.catapult_left
    weight.catapult_left = 0
    weight.save()

    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_add_last(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    target = get_object_or_404(models.TargetVertex, pk=id2)
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    if not models.WeightModel.objects.filter(target=target).exists():
        order = 0
    else:
        order = (
            models.WeightModel.objects.filter(target=target).aggregate(Max("order"))[
                "order__max"
            ]
            + 1
        )
    models.WeightModel.objects.create(
        target=target,
        player=weight.player,
        start=weight.start,
        state=weight,
        off=weight.off_left,
        catapult=weight.catapult_left,
        nobleman=weight.nobleman_left,
        order=order,
        distance=round(
            basic.Village(target.target).distance(basic.Village(weight.start)),
            1,
        ),
        first_line=weight.first_line,
    )
    weight.off_state += weight.off_left
    weight.off_left = 0
    weight.nobleman_state += weight.nobleman_left
    weight.nobleman_left = 0
    weight.catapult_state += weight.catapult_left
    weight.catapult_left = 0
    weight.save()

    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_move_down(
    request: HttpRequest, id1: int, id2: int, id4: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
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
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_move_up(request: HttpRequest, id1: int, id2: int, id4: int) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)

    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
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
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_weight_delete(
    request: HttpRequest, id1: int, id2: int, id4: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    weight_model: models.WeightModel = models.WeightModel.objects.select_related(
        "state"
    ).filter(pk=id4)[0]
    state: models.WeightMaximum = weight_model.state
    state.off_left += weight_model.off
    state.off_state -= weight_model.off

    state.nobleman_left += weight_model.nobleman
    state.nobleman_state -= weight_model.nobleman
    state.catapult_left += weight_model.catapult
    state.catapult_state -= weight_model.catapult
    state.save()
    weight_model.delete()

    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_divide(
    request: HttpRequest, id1: int, id2: int, id4: int, n: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    weight: models.WeightModel = models.WeightModel.objects.select_related(
        "state"
    ).filter(pk=id4)[0]
    n_list = [i + 1 for i in range(n - 1)]
    nob_list = [i for i in range(max(weight.nobleman - 1, 0))]
    if n > weight.nobleman:
        zipped_list = zip_longest(n_list, nob_list)
        nob_number = max(weight.nobleman - 1, 0)
    else:
        zipped_list = zip(n_list, nob_list)
        nob_number = n - 1

    off = weight.off // n
    catapult = weight.catapult // n
    rest = weight.off - off * n
    rest_catapult = weight.catapult - catapult * n
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
                ruin=weight.ruin,
                catapult=catapult,
                nobleman=nob,
                order=weight.order + number,
                distance=weight.distance,
                first_line=weight.first_line,
            )
        )
    weight.off = off + rest
    weight.catapult = catapult + rest_catapult
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
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )


@require_POST
@login_required
def initial_hide_weight(
    request: HttpRequest, id1: int, id2: int, id3: int
) -> HttpResponse:
    outline = get_object_or_404(models.Outline, owner=request.user, id=id1)
    target = get_object_or_404(models.TargetVertex, pk=id2)
    sort = request.GET.get("sort")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr")
    weight = get_object_or_404(models.WeightMaximum, pk=id3)
    weight.hidden = not weight.hidden
    weight.save()
    return redirect(
        reverse("base:planer_initial_detail", args=[id1, id2])
        + f"?page={page}&sort={sort}&filtr={filtr}"
    )
