from time import time
from typing import Optional, Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import Max, Sum
from django.forms import formset_factory
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import get_language, gettext
from django.views.decorators.http import require_POST
from markdownx.utils import markdownify

import utils.avaiable_troops as avaiable_troops
import utils.basic as basic
from base import forms, models
from utils.outline_complete import complete_outline_write
from utils.outline_create_targets import OutlineCreateTargets
from utils.outline_finish import MakeFinalOutline
from utils.outline_initial import MakeOutline


@login_required
def initial_form(request: HttpRequest, _id: int) -> HttpResponse:
    """
    view with table with created outline,

    returned after valid filled form earlier

    """
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )
    if instance.off_troops == "":
        request.session["error"] = gettext("<h5>Army collection is empty!</h5>")
        return redirect("base:planer_detail", _id)
    if instance.written == "active":
        return redirect("base:planer_initial", _id)
    premium_error: bool
    if request.session.get("premium_error") is True:
        premium_error = True
        del request.session["premium_error"]
    else:
        premium_error = False

    language_code = get_language()

    info = models.Documentation.objects.get_or_create(
        title="planer_form_info",
        language=language_code,
        defaults={"main_page": ""},
    )[0].main_page
    info = markdownify(info)

    example = models.Documentation.objects.get_or_create(
        title="planer_form_example",
        language=language_code,
        defaults={"main_page": ""},
    )[0].main_page
    example = markdownify(example)

    if models.WeightMaximum.objects.filter(outline=instance).count() == 0:

        off_form = forms.OffTroopsForm(
            {"off_troops": instance.off_troops}, outline=instance
        )
        if off_form.is_valid():
            make_outline = MakeOutline(outline=instance)
            make_outline()
        else:
            request.session["error"] = gettext(
                "<h5>It looks like your Army collection is no longer actual!</h5> <p>To use the Planer:</p> <p>1. Paste the current data in the <b>Army collection</b> and <b>Submit</b>.</p> <p>2. Return to the <b>Planer</b> tab.</p> <p>3. Navigate to the header <span class='md-correct'>Updating off troops</span> at the bottom of page.</p><p>4. Click the button <span class='md-correct'>Recreate models</span>.</p>"
            )

            return redirect("base:planer_detail", _id)

    target_mode = basic.TargetMode(request.GET.get("t"))

    form1 = forms.InitialOutlineForm(None, outline=instance, target_mode=target_mode)
    form2 = forms.AvailableTroopsForm(None)
    form3 = forms.SettingDateForm(None)
    form4 = forms.ModeOutlineForm(None)
    form5 = forms.NightBonusSetForm(None)
    form6 = forms.RuiningOutlineForm(None)

    calculations: basic.CalcultateDuplicates = basic.CalcultateDuplicates(
        outline=instance, target_mode=target_mode
    )

    len_fake = calculations.len_fake
    len_ruin = calculations.len_ruin
    len_real = calculations.len_real

    estimated_time = 12 * (len_real + len_fake) + 50 * len_ruin  # type: ignore

    real_dups = calculations.real_duplicates()
    fake_dups = calculations.fake_duplicates()
    ruin_dups = calculations.ruin_duplicates()

    if target_mode.is_real:
        form1.fields["target"].initial = instance.initial_outline_targets
    elif target_mode.is_fake:
        form1.fields["target"].initial = instance.initial_outline_fakes
    else:
        form1.fields["target"].initial = instance.initial_outline_ruins

    form2.fields[
        "initial_outline_front_dist"
    ].initial = instance.initial_outline_front_dist
    form2.fields[
        "initial_outline_maximum_front_dist"
    ].initial = instance.initial_outline_maximum_front_dist
    form2.fields[
        "initial_outline_target_dist"
    ].initial = instance.initial_outline_target_dist
    form2.fields["initial_outline_min_off"].initial = instance.initial_outline_min_off
    form2.fields[
        "initial_outline_excluded_coords"
    ].initial = instance.initial_outline_excluded_coords
    form3.fields["date"].initial = ""
    form4.fields["mode_off"].initial = instance.mode_off
    form4.fields["mode_noble"].initial = instance.mode_noble
    form4.fields["mode_division"].initial = instance.mode_division
    form4.fields["mode_guide"].initial = instance.mode_guide
    form4.fields["mode_split"].initial = instance.mode_split
    form4.fields[
        "initial_outline_fake_limit"
    ].initial = instance.initial_outline_fake_limit
    form4.fields[
        "initial_outline_fake_mode"
    ].initial = instance.initial_outline_fake_mode

    form5.fields["night_bonus"].initial = instance.night_bonus
    form5.fields["enter_t1"].initial = instance.enter_t1
    form5.fields["enter_t2"].initial = instance.enter_t2

    form6.fields[
        "initial_outline_off_left_catapult"
    ].initial = instance.initial_outline_off_left_catapult
    form6.fields[
        "initial_outline_catapult_default"
    ].initial = instance.initial_outline_catapult_default
    form6.fields[
        "initial_outline_average_ruining_points"
    ].initial = instance.initial_outline_average_ruining_points

    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.InitialOutlineForm(
                request.POST, outline=instance, target_mode=target_mode
            )
            if form1.is_valid():
                off_form = forms.OffTroopsForm(
                    {"off_troops": instance.off_troops}, outline=instance
                )
                if off_form.is_valid():
                    instance.save()
                    create_targets = OutlineCreateTargets(instance, target_mode)
                    create_targets()
                else:
                    request.session["error"] = gettext(
                        "<h5>It looks like your Army collection is no longer actual!</h5> <p>To use the Planer:</p> <p>1. Paste the current data in the <b>Army collection</b> and <b>Submit</b>.</p> <p>2. Return to the <b>Planer</b> tab.</p> <p>3. Navigate to the header <span class='md-correct'>Updating off troops</span> at the bottom of page.</p><p>4. Click the button <span class='md-correct'>Recreate models</span>.</p>"
                    )
                    return redirect("base:planer_detail", _id)

                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form2" in request.POST:
            form2 = forms.AvailableTroopsForm(request.POST)
            if form2.is_valid():
                min_off = request.POST.get("initial_outline_min_off")
                radius_min = request.POST.get("initial_outline_front_dist")
                radius_max = request.POST.get("initial_outline_maximum_front_dist")

                radius_target = request.POST.get("initial_outline_target_dist")
                excluded_coords = request.POST.get("initial_outline_excluded_coords")
                instance.initial_outline_min_off = min_off
                instance.initial_outline_front_dist = radius_min
                instance.initial_outline_maximum_front_dist = radius_max
                instance.initial_outline_target_dist = radius_target
                instance.initial_outline_excluded_coords = excluded_coords
                instance.save()
                avaiable_troops.get_legal_coords_outline(outline=instance)
                avaiable_troops.update_available_ruins(outline=instance)
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form3" in request.POST:
            form3 = forms.SettingDateForm(request.POST)
            if form3.is_valid():
                date = request.POST.get("date")
                instance.date = date
                instance.save()
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form4" in request.POST:
            form4 = forms.ModeOutlineForm(request.POST)
            if form4.is_valid():
                mode_off = request.POST.get("mode_off")
                mode_noble = request.POST.get("mode_noble")
                mode_division = request.POST.get("mode_division")
                mode_guide = request.POST.get("mode_guide")
                fake_limit = request.POST.get("initial_outline_fake_limit")
                mode_split = request.POST.get("mode_split")
                initial_outline_fake_mode = request.POST.get(
                    "initial_outline_fake_mode"
                )

                instance.mode_off = mode_off
                instance.mode_noble = mode_noble
                instance.mode_division = mode_division
                instance.mode_guide = mode_guide
                instance.mode_split = mode_split
                instance.initial_outline_fake_limit = fake_limit
                instance.initial_outline_fake_mode = initial_outline_fake_mode

                instance.save()

                models.TargetVertex.objects.filter(outline=instance).update(
                    mode_off=mode_off,
                    mode_noble=mode_noble,
                    mode_division=mode_division,
                    mode_guide=mode_guide,
                )
                models.WeightMaximum.objects.filter(outline=instance).update(
                    fake_limit=fake_limit
                )

                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form5" in request.POST:
            form5 = forms.NightBonusSetForm(request.POST)
            if form5.is_valid():
                night_bonus = request.POST.get("night_bonus")
                if night_bonus == "on":
                    night_bonus = True
                else:
                    night_bonus = False
                enter_t1: Optional[str] = request.POST.get("enter_t1")
                enter_t2: Optional[str] = request.POST.get("enter_t2")
                instance.night_bonus = night_bonus
                instance.enter_t1 = enter_t1
                instance.enter_t2 = enter_t2
                instance.save()
                models.TargetVertex.objects.filter(outline=instance).update(
                    night_bonus=night_bonus,
                    enter_t1=enter_t1,
                    enter_t2=enter_t2,
                )
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form6" in request.POST:
            form6 = forms.RuiningOutlineForm(request.POST)
            if form6.is_valid():
                catapult_default: Optional[str] = request.POST.get(
                    "initial_outline_catapult_default"
                )
                catapult_left: Optional[str] = request.POST.get(
                    "initial_outline_off_left_catapult"
                )
                initial_outline_average_ruining_points: Optional[
                    str
                ] = request.POST.get("initial_outline_average_ruining_points")

                instance.initial_outline_catapult_default = catapult_default
                instance.initial_outline_off_left_catapult = catapult_left
                instance.initial_outline_average_ruining_points = (
                    initial_outline_average_ruining_points
                )

                instance.save()
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

    context = {
        "instance": instance,
        "form1": form1,
        "example": example,
        "info": info,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form5": form5,
        "form6": form6,
        "fake_dups": fake_dups,
        "real_dups": real_dups,
        "ruin_dups": ruin_dups,
        "mode": target_mode.mode,
        "len_real": len_real,
        "len_fake": len_fake,
        "len_ruin": len_ruin,
        "estimated_time": estimated_time,
        "premium_error": premium_error,
    }
    return render(request, "base/new_outline/new_outline_initial_period1.html", context)


@login_required
def initial_planer(request: HttpRequest, _id: int) -> HttpResponse:  # type: ignore
    """view with form for initial period outline"""
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )
    if instance.written == "inactive":
        raise Http404()

    filter_form = forms.SetTargetsMenuFilters(None)
    filter_form.fields["filter_targets_number"].initial = instance.filter_targets_number
    filter_form.fields["simple_textures"].initial = instance.simple_textures
    mode: basic.Mode = basic.Mode(request.GET.get("mode"))
    page_number = request.GET.get("page")
    filtr = request.GET.get("filtr") or ""

    if request.method == "POST":
        if "form1" in request.POST:
            instance.remove_user_outline()
            return redirect("base:planer_initial_form", _id)

        if "form-filter-targets" in request.POST:
            filter_form = forms.SetTargetsMenuFilters(request.POST)
            if filter_form.is_valid():
                cards = request.POST.get("filter_targets_number")
                if request.POST.get("simple_textures") == "on":
                    textures = True
                else:
                    textures = False
                instance.filter_targets_number = cards
                instance.simple_textures = textures
                instance.save()
                return redirect(
                    reverse("base:planer_initial", args=[_id])
                    + f"?page={page_number}&mode={mode}&filtr={filtr}"
                )
        if "create" in request.POST:
            # add_and_remove tab only

            profile: models.Profile = models.Profile.objects.get(user=request.user)
            is_premium: bool = profile.is_premium()

            target_form = forms.CreateNewInitialTarget(
                request.POST, outline=instance, is_premium=is_premium
            )
            if target_form.is_valid():
                target_type = request.POST.get("target_type")
                target_coord = request.POST.get("target")
                instance.create_target(target_type=target_type, coord=target_coord)

                request.session["success"] = "success"

                return redirect(
                    reverse("base:planer_initial", args=[_id])
                    + f"?page={page_number}&mode={mode}&filtr={filtr}"
                )

    if not mode.is_time:

        page_obj = instance.pagin_targets(
            page=page_number,
            fake=mode.is_fake,
            ruin=mode.is_ruin,
            every=mode.is_add_and_remove,
            filtr=filtr,
        )
        query = instance.targets_query(target_lst=page_obj)

        context = {
            "instance": instance,
            "query": query,
            "page_obj": page_obj,
            "mode": mode,
            "filter_form": filter_form,
            "filtr": filtr,
        }
        if mode.is_add_and_remove:
            message: Optional[str] = request.session.get("success")
            if message is not None:
                del request.session["success"]

            if request.method == "POST":
                target_form = forms.CreateNewInitialTarget(
                    request.POST, outline=instance, is_premium=True
                )
            else:
                target_form = forms.CreateNewInitialTarget(
                    None, outline=instance, is_premium=True
                )

            context["target_form"] = target_form
            context["message"] = message

        return render(
            request,
            "base/new_outline/new_outline_initial_period2.html",
            context,
        )

    elif mode.is_time:
        error: Optional[str] = request.session.get("outline_error")
        if error is not None:
            del request.session["outline_error"]

        page_obj = instance.pagin_targets(
            page=page_number,
            every=True,
            not_empty_only=True,
            related=True,
            filtr=filtr,
        )
        query = instance.targets_query(target_lst=page_obj)
        outline_time_dict = instance.get_outline_times(with_periods=True)

        select_formset = formset_factory(
            form=forms.ChooseOutlineTimeForm, extra=12, max_num=12
        )

        create_formset = formset_factory(
            form=forms.PeriodForm,
            formset=forms.BasePeriodFormSet,
            extra=6,
            min_num=2,
            max_num=6,
        )

        if request.method == "POST":
            if "form-finish" in request.POST:
                if instance.is_target_with_no_time():
                    request.session["outline_error"] = gettext(
                        "<h5>All targets must have an assigned Time.</h5>"
                    )
                    return redirect(
                        reverse("base:planer_initial", args=[_id]) + "?page=1&mode=time"
                    )
                models.Overview.objects.filter(outline=instance).update(removed=True)
                make_final_outline = MakeFinalOutline(instance)

                error_messages = make_final_outline()
                if len(error_messages) > 0:
                    request.session["error_messages"] = ",".join(error_messages)

                return redirect("base:planer_detail_results", _id)

            if "formset" in request.POST:
                create_formset = create_formset(request.POST)
                select_formset = select_formset()
                if create_formset.is_valid():
                    outline_times_Q = models.OutlineTime.objects.filter(
                        outline=instance
                    )
                    if outline_times_Q.count() == 0:
                        order = 1
                    else:
                        order = (
                            outline_times_Q.aggregate(Max("order"))["order__max"] + 1
                        )

                    new_time = models.OutlineTime.objects.create(
                        outline=instance, order=order
                    )
                    create_list = []
                    for obj_dict in create_formset.cleaned_data:
                        if obj_dict == {}:
                            continue
                        obj_dict["outline_time"] = new_time
                        create_list.append(models.PeriodModel(**obj_dict))
                    models.PeriodModel.objects.bulk_create(create_list)
                    return redirect(
                        reverse("base:planer_initial", args=[_id])
                        + f"?page={page_number}&mode={mode}&filtr={filtr}"
                    )
                else:
                    for form in create_formset:
                        for err in form.errors:
                            form.fields[err].widget.attrs["class"] += " border-invalid"

        else:
            create_formset = create_formset()

        context = {
            "instance": instance,
            "outline_time": outline_time_dict,
            "query": query,
            "page_obj": page_obj,
            "mode": mode,
            "filter_form": filter_form,
            "formset": create_formset,
            "choice_formset": select_formset,
            "error": error,
            "filtr": filtr,
        }

        return render(
            request,
            "base/new_outline/new_outline_initial_period2_1.html",
            context,
        )


@login_required
def initial_target(request: HttpRequest, id1: int, id2: int) -> HttpResponse:
    """view with form for initial period outline detail"""
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=id1, owner=request.user
    )
    if instance.written == "inactive":
        raise Http404()

    target = get_object_or_404(models.TargetVertex, pk=id2)
    village_id = models.VillageModel.objects.get(
        world=instance.world, coord=target.target
    ).village_id

    link_to_tw = instance.world.tw_stats_link_to_village(village_id)

    result_lst = (
        models.WeightModel.objects.select_related("state")
        .filter(target=target)
        .order_by("order")
    )
    for weight in result_lst:
        weight.distance = round(weight.distance, 1)
    # sort
    sort_obj = basic.SortAndPaginRequest(
        outline=instance,
        request_GET_sort=request.GET.get("sort"),
        request_GET_page=request.GET.get("page"),
        request_GET_filtr=request.GET.get("filtr"),
        target=target,
    )
    page_obj = sort_obj.sorted_query()

    sort = sort_obj.sort
    filtr = sort_obj.filtr
    # Forms
    filter_form = forms.SetNewOutlineFilters(request.POST or None)
    filter_form.fields["filter_weights_min"].initial = instance.filter_weights_min
    filter_form.fields["filter_weights_max"].initial = instance.filter_weights_max
    filter_form.fields["filter_card_number"].initial = instance.filter_card_number
    filter_form.fields["filter_hide_front"].initial = instance.filter_hide_front

    if request.method == "POST":
        if "form-filter" in request.POST:
            if filter_form.is_valid():
                minimum = request.POST.get("filter_weights_min")
                maximum = request.POST.get("filter_weights_max")
                cards = request.POST.get("filter_card_number")
                hide_front = request.POST.get("filter_hide_front")

                instance.filter_weights_min = minimum
                instance.filter_weights_max = maximum
                instance.filter_card_number = cards
                instance.filter_hide_front = hide_front
                instance.save()
                return redirect(
                    reverse("base:planer_initial_detail", args=[id1, id2])
                    + f"?page={page_obj.number}&sort={sort}&filtr={filtr}"
                )

        if "form" in request.POST:
            form = forms.WeightForm(request.POST)
            if form.is_valid():
                weight_id: Optional[str] = request.POST.get("weight_id")
                off_post: Optional[str] = request.POST.get("off")
                nobleman_post: Optional[str] = request.POST.get("nobleman")
                if nobleman_post is not None and off_post is not None:
                    nobleman = int(nobleman_post)
                    off = int(off_post)
                else:
                    raise Http404()
                weight: models.WeightModel = get_object_or_404(
                    models.WeightModel.objects.select_related("state"), pk=weight_id
                )
                state: models.WeightMaximum = weight.state
                off_diffrence: int = off - weight.off
                noble_diffrence: int = nobleman - weight.nobleman

                state.off_state += off_diffrence
                state.off_left -= off_diffrence
                state.nobleman_state += noble_diffrence
                state.nobleman_left -= noble_diffrence

                off_additional: int = 0
                if off > weight.off:
                    if off > weight.off + state.off_left - state.catapult_left * 8:
                        off_from_catapults: int = weight.off + state.off_left - off
                        catapults_up: int = min(
                            (off_from_catapults // 8) + 1, state.catapult_left
                        )
                        state.catapult_state += catapults_up
                        state.catapult_left -= catapults_up
                        state.off_state += catapults_up * 8 - off_from_catapults
                        state.off_left -= catapults_up * 8 - off_from_catapults
                        off_additional = catapults_up * 8 - off_from_catapults
                    else:
                        catapults_up = 0
                    catapults = weight.catapult + catapults_up
                else:
                    if weight.catapult * 8 > off:
                        off_from_catapults: int = weight.catapult * 8 - off
                        catapults_down: int = min(
                            (off_from_catapults // 8) + 1, weight.catapult
                        )
                        state.catapult_state -= catapults_down
                        state.catapult_left += catapults_down
                        state.off_state -= catapults_down * 8 - off_from_catapults
                        state.off_left += catapults_down * 8 - off_from_catapults
                        off_additional = off_from_catapults - catapults_down * 8
                    else:
                        catapults_down: int = 0
                    catapults = weight.catapult - catapults_down

                weight.off = off + off_additional
                weight.nobleman = nobleman
                weight.catapult = catapults

                weight.save()
                state.save()
                return redirect(
                    reverse("base:planer_initial_detail", args=[id1, id2])
                    + f"?page={page_obj.number}&sort={sort}&filtr={filtr}"
                )
        else:
            form = forms.WeightForm(None)

    else:
        form = forms.WeightForm(None)

    paint: Optional[str] = request.session.get("weight")
    if paint is not None:
        try:
            paint_id: int = int(paint)
        except ValueError:
            pass
        else:
            for model in result_lst:
                if model.id == paint_id:
                    model.paint = "paint"
                    break
        finally:
            del request.session["weight"]

    context = {
        "filter_form": filter_form,
        "link": link_to_tw,
        "instance": instance,
        "target": target,
        "result_lst": result_lst,
        "form": form,
        "page_obj": page_obj,
        "sort": sort,
        "paint": paint,
        "filtr": filtr,
    }

    return render(
        request,
        "base/new_outline/new_outline_initial_period3.html",
        context,
    )


@require_POST
@login_required
def initial_delete_time(request: HttpRequest, pk: int) -> HttpResponse:
    outline_time: models.OutlineTime = get_object_or_404(
        models.OutlineTime.objects.select_related(), pk=pk
    )
    outline: models.Outline = get_object_or_404(
        models.Outline, owner=request.user, id=outline_time.outline.id
    )
    mode: Optional[str] = request.GET.get("mode")
    page: Optional[str] = request.GET.get("page")
    if outline.default_off_time_id == outline_time.pk:
        outline.default_off_time_id = None
    if outline.default_fake_time_id == outline_time.pk:
        outline.default_fake_time_id = None
    if outline.default_ruin_time_id == outline_time.pk:
        outline.default_ruin_time_id = None

    outline.save()
    outline_time.delete()
    return redirect(
        reverse("base:planer_initial", args=[outline.pk]) + f"?page={page}&mode={mode}"
    )


@login_required
@require_POST
def initial_set_all_time(request: HttpRequest, pk: int) -> HttpResponse:
    outline_time: models.OutlineTime = get_object_or_404(
        models.OutlineTime.objects.select_related(), pk=pk
    )
    outline: models.Outline = get_object_or_404(
        models.Outline, owner=request.user, id=outline_time.outline.id
    )
    mode: Optional[str] = request.GET.get("mode")
    page: Optional[str] = request.GET.get("page")
    fake: Optional[str] = request.GET.get("fake")
    ruin: Optional[str] = request.GET.get("ruin")

    if fake == "true":
        fake_state: bool = True
        ruin_state: bool = False
        outline.default_fake_time_id = outline_time.pk
    elif ruin == "true":
        fake_state: bool = False
        ruin_state: bool = True
        outline.default_ruin_time_id = outline_time.pk
    else:
        fake_state: bool = False
        ruin_state: bool = False
        outline.default_off_time_id = outline_time.pk

    targets = models.TargetVertex.objects.filter(
        outline=outline, fake=fake_state, ruin=ruin_state
    )
    targets.update(outline_time=outline_time)
    outline.save()

    return redirect(
        reverse("base:planer_initial", args=[outline.pk]) + f"?page={page}&mode={mode}"
    )


@login_required
@require_POST
def complete_outline(request: HttpRequest, id1: int) -> HttpResponse:
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=id1, owner=request.user
    )
    user: Union[AbstractBaseUser, AnonymousUser] = request.user
    profile: models.Profile = models.Profile.objects.get(user=user)
    if not profile.is_premium():
        target_mode: Optional[str] = request.GET.get("t")
        target_count: int = models.TargetVertex.objects.filter(outline=instance).count()
        if target_count > 25:
            request.session["premium_error"] = True
            return redirect(
                reverse("base:planer_initial_form", args=[id1]) + f"?t={target_mode}"
            )

    complete_outline_write(outline=instance)
    instance.written = "active"
    instance.save()
    return redirect(reverse("base:planer_initial", args=[id1]) + "?page=1&mode=menu")


@login_required
@require_POST
def update_outline_troops(request: HttpRequest, id1: int) -> HttpResponse:
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=id1, owner=request.user
    )
    off_form: forms.OffTroopsForm = forms.OffTroopsForm(
        {"off_troops": instance.off_troops}, outline=instance
    )
    if off_form.is_valid():
        make_outline = MakeOutline(instance)
        make_outline()
    else:
        request.session["error"] = gettext(
            "<h5>It looks like your Army collection is no longer actual!</h5> <p>To use the Planer:</p> <p>1. Paste the current data in the <b>Army collection</b> and <b>Submit</b>.</p> <p>2. Return to the <b>Planer</b> tab.</p> <p>3. Navigate to the header <span class='md-correct'>Updating off troops</span> at the bottom of page.</p><p>4. Click the button <span class='md-correct'>Recreate models</span>.</p>"
        )

        return redirect("base:planer_detail", id1)
    target_mode = basic.TargetMode(request.GET.get("t"))
    instance.avaiable_offs = []
    instance.avaiable_offs_near = []
    instance.avaiable_nobles = []
    instance.avaiable_nobles_near = []
    instance.avaiable_ruins = None
    instance.save()
    return redirect(
        reverse("base:planer_initial_form", args=[id1]) + f"?t={target_mode.mode}"
    )
