from collections import Counter

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.utils.translation import gettext
from django.db.models import Max
from django.utils.translation import get_language
from markdownx.utils import markdownify

import tribal_wars.outline_initial as initial
import tribal_wars.outline_finish as finish
import tribal_wars.basic as basic
import tribal_wars.avaiable_troops as avaiable_troops
from base import models, forms


@login_required
def initial_form(request, _id):
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

        off_form = forms.OffTroopsForm({"off_troops": instance.off_troops}, outline=instance)
        if off_form.is_valid():
            initial.make_outline(instance, make_targets=False)
        else:
            request.session["error"] = gettext("<h5>It looks like your Army collection is no longer actual!</h5> <p>To use the Planer:</p> <p>1. Paste the current data in the <b>Army collection</b> and <b>Submit</b>.</p> <p>2. Return to the <b>Planer</b> tab.</p> <p>3. Expand first tab <span class='md-correct2'>1. Available Troops</span>.</p> <p>4. Click the button <span class='md-correct2'>Click here to update if u have changed Army troops</span>.</p>")

            return redirect("base:planer_detail", _id)

    form1 = forms.InitialOutlineForm(None, outline=instance)

    form2 = forms.AvailableTroopsForm(None)
    form3 = forms.SettingDateForm(None)
    form4 = forms.ModeOutlineForm(None)
    form5 = forms.NightBonusSetForm(None)
    targets = models.TargetVertex.objects.filter(outline=instance).order_by("id")
    len_targets = len(targets)

    target_dups = [(coord, nums) for coord, nums in Counter([target.target for target in targets if not target.fake]).items() if nums > 1]
    fake_dups = [(coord, nums) for coord, nums in Counter([target.target for target in targets if target.fake]).items() if nums > 1]

    if len_targets <= 100:
        formset_select = formset_factory(
            form=forms.ModeTargetSetForm, extra=len_targets, max_num=len_targets
        )
    else:
        formset_select = None

    form1.fields["target"].initial = instance.initial_outline_targets
    form2.fields[
        "initial_outline_front_dist"
    ].initial = instance.initial_outline_front_dist
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
    form5.fields["night_bonus"].initial = instance.night_bonus
    form5.fields["enter_t1"].initial = instance.enter_t1
    form5.fields["enter_t2"].initial = instance.enter_t2
    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.InitialOutlineForm(request.POST, outline=instance)
            if form1.is_valid():
                off_form1 = forms.OffTroopsForm({"off_troops": instance.off_troops}, outline=instance)
                if off_form1.is_valid():
                    initial.make_outline(instance, make_targets=True)
                else:
                    request.session["error"] = gettext("<h5>It looks like your Army collection is no longer actual!</h5> <p>To use the Planer:</p> <p>1. Paste the current data in the <b>Army collection</b> and <b>Submit</b>.</p> <p>2. Return to the <b>Planer</b> tab.</p> <p>3. Expand first tab <span class='md-correct2'>1. Available Troops</span>.</p> <p>4. Click the button <span class='md-correct2'>Click here to update if u have changed Army troops</span>.</p>")
                    return redirect("base:planer_detail", _id)
                instance.save()
                return redirect("base:planer_initial_form", _id)

        if "form2" in request.POST:
            form2 = forms.AvailableTroopsForm(request.POST)
            if form2.is_valid():
                min_off = request.POST.get("initial_outline_min_off")
                radius = request.POST.get("initial_outline_front_dist")
                radius_target = request.POST.get("initial_outline_target_dist")
                excluded_coords = request.POST.get("initial_outline_excluded_coords")
                instance.initial_outline_min_off = min_off
                instance.initial_outline_front_dist = radius
                instance.initial_outline_target_dist = radius_target
                instance.initial_outline_excluded_coords = excluded_coords
                instance.save()
                avaiable_troops.get_legal_coords_outline(outline=instance)
                avaiable_troops.legal_coords_near_targets(outline=instance)
                return redirect("base:planer_initial_form", _id)

        if "form3" in request.POST:
            form3 = forms.SettingDateForm(request.POST)
            if form3.is_valid():
                date = request.POST.get("date")
                instance.date = date
                instance.save()
                return redirect("base:planer_initial_form", _id)

        if "form4" in request.POST:
            form4 = forms.ModeOutlineForm(request.POST)
            if form4.is_valid():
                mode_off = request.POST.get("mode_off")
                mode_noble = request.POST.get("mode_noble")
                mode_division = request.POST.get("mode_division")
                mode_guide = request.POST.get("mode_guide")
                fake_limit = request.POST.get("initial_outline_fake_limit")
                mode_split = request.POST.get("mode_split")
                instance.mode_off = mode_off
                instance.mode_noble = mode_noble
                instance.mode_division = mode_division
                instance.mode_guide = mode_guide
                instance.mode_split = mode_split
                instance.initial_outline_fake_limit = fake_limit
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

                return redirect("base:planer_initial_form", _id)

        if "form5" in request.POST:
            form5 = forms.NightBonusSetForm(request.POST)
            if form5.is_valid():
                night_bonus = request.POST.get("night_bonus")
                if night_bonus == "on":
                    night_bonus = True
                else:
                    night_bonus = False
                enter_t1 = request.POST.get("enter_t1")
                enter_t2 = request.POST.get("enter_t2")
                instance.night_bonus = night_bonus
                instance.enter_t1 = enter_t1
                instance.enter_t2 = enter_t2
                instance.save()
                models.TargetVertex.objects.filter(outline=instance).update(
                    night_bonus = night_bonus,
                    enter_t1 = enter_t1,
                    enter_t2 = enter_t2,
                )
                return redirect("base:planer_initial_form", _id)

        if "formset" in request.POST and formset_select is not None:
            formset_select = formset_select(request.POST)
            if formset_select.is_valid():
                targets_to_update = []
                for data, target in zip(formset_select.cleaned_data, targets):
                    if data == {}:
                        continue
                    target.mode_off = data["mode_off"]
                    target.mode_noble = data["mode_noble"]
                    target.mode_division = data["mode_division"]
                    target.mode_guide = data["mode_guide"]
                    targets_to_update.append(target)
                models.TargetVertex.objects.bulk_update(
                    targets_to_update,
                    fields=[
                        "mode_off",
                        "mode_noble",
                        "mode_division",
                        "mode_guide",
                    ],
                )
                return redirect("base:planer_initial_form", _id)
        else:
            if formset_select is not None:
                formset_select = formset_select(None)
    else:
        if formset_select is not None:
            formset_select = formset_select(None)
    if formset_select is not None:
        for form, target in zip(formset_select, targets):
            form.target = target
            form.fields["mode_off"].initial = target.mode_off
            form.fields["mode_noble"].initial = target.mode_noble
            form.fields["mode_division"].initial = target.mode_division
            form.fields["mode_guide"].initial = target.mode_guide

    context = {
        "instance": instance,
        "form1": form1,
        "example": example,
        "info": info,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form5": form5,
        "formset": formset_select,
        "fake_dups": fake_dups,
        "target_dups": target_dups,
    }
    return render(request, "base/new_outline/new_outline_initial_period1.html", context)


@login_required
def initial_planer(request, _id):
    """ view with form for initial period outline """
    instance = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )
    if instance.written == "inactive":
        return Http404()
    if request.method == "POST":
        if "form1" in request.POST:
            instance.remove_user_outline()
            return redirect("base:planer_initial_form", _id)

    mode = basic.Mode(request.GET.get("mode"))

    if mode.is_menu:
        queries = basic.TargetWeightQueries(outline=instance, fake=False)
        target_dict = queries.target_dict_with_weights_read()
        paginator = Paginator(list(target_dict.items()), 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {"instance": instance, "query": page_obj, "mode": str(mode)}

        return render(
            request,
            "base/new_outline/new_outline_initial_period2.html",
            context,
        )

    elif mode.is_fake:
        queries = basic.TargetWeightQueries(outline=instance, fake=True)
        target_dict = queries.target_dict_with_weights_read()
        paginator = Paginator(list(target_dict.items()), 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {"instance": instance, "query": page_obj, "mode": str(mode)}

        return render(
            request,
            "base/new_outline/new_outline_initial_period2_2.html",
            context,
        )

    elif mode.is_add_and_remove:
        queries = basic.TargetWeightQueries(outline=instance, every=True)
        target_dict = queries.target_dict_with_weights_read()
        for target, lst in target_dict.items():
            number = len(lst)
            target_dict[target] = number
        reals = len([target for target in target_dict if target.fake == False])
        fakes = len([target for target in target_dict if target.fake == True])

        paginator = Paginator(list(target_dict.items()), 20)
        page_number = request.GET.get("page")
        message = request.session.get("success")
        if message:
            del request.session["success"]
        page_obj = paginator.get_page(page_number)

        if request.method == "POST":
            if "create" in request.POST:
                target_form = forms.CreateNewInitialTarget(
                    request.POST, outline=instance
                )
                if target_form.is_valid():
                    fake = request.POST.get("fake")
                    if fake == "on":
                        fake = True
                    if fake is None:
                        fake = False
                    coord = request.POST.get("target")

                    village = models.VillageModel.objects.select_related().get(
                        coord=coord, world=instance.world
                    )

                    models.TargetVertex.objects.create(
                        outline=instance,
                        player=village.player.name,
                        target=coord,
                        fake=fake,
                    )
                    request.session["success"] = "success"
                    return redirect(
                        reverse("base:planer_initial", args=[_id])
                        + f"?page={page_obj.number}&mode={str(mode)}"
                    )
            else:
                target_form = forms.CreateNewInitialTarget(None, outline=instance)
        else:
            target_form = forms.CreateNewInitialTarget(None, outline=instance)

        context = {
            "message": message,
            "target_form": target_form,
            "instance": instance,
            "query": page_obj,
            "mode": str(mode),
            "fakes": fakes,
            "reals": reals,
        }

        return render(
            request,
            "base/new_outline/new_outline_initial_period2_3.html",
            context,
        )

    elif mode.is_time:
        queries = basic.TargetWeightQueries(outline=instance, every=True)
        try:
            error = request.session["outline_error"]
        except KeyError:
            error = None
        else:
            del request.session["outline_error"]
        time_id_and_periods = queries.time_period_dictionary()

        dict_order_to_time_obj = time_id_and_periods[0]
        dict_time_obj_to_periods = time_id_and_periods[1]
        dict_target_to_weights = queries.target_dict_with_weights_read()

        paginator = Paginator(list(dict_target_to_weights.items()), 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        choices = [
            (f"{time.order}", f"{time.order}") for time in dict_time_obj_to_periods
        ]

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
                target_with_no_time = (
                    models.TargetVertex.objects.filter(outline=instance)
                    .filter(outline_time=None)
                    .exists()
                )
                if target_with_no_time:
                    request.session["outline_error"] = gettext(
                        "<h5>All targets must have an assigned Time.</h5>"
                    )
                    return redirect(
                        reverse("base:planer_initial", args=[_id]) + "?page=1&mode=time"
                    )
                models.Overview.objects.filter(outline=instance).update(removed=True)
                finish.make_final_outline(instance)
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
                        + f"?page={page_obj.number}&mode={str(mode)}"
                    )
                else:
                    for form in create_formset:
                        for err in form.errors:
                            form.fields[err].widget.attrs["class"] += " border-invalid"

            if "choice-formset" in request.POST:
                select_formset = select_formset(request.POST)
                for form in select_formset.forms:
                    form.fields["choice"].choices = choices
                create_formset = create_formset()
                if select_formset.is_valid():
                    update_list = []
                    for data, tup in zip(select_formset.cleaned_data, page_obj):
                        try:
                            index = int(data["choice"])
                        except KeyError:
                            continue
                        else:
                            outline_time = dict_order_to_time_obj[index]

                        if tup[0].outline_time != outline_time:
                            tup[0].outline_time = outline_time
                            update_list.append(tup[0])
                    models.TargetVertex.objects.bulk_update(
                        update_list, ["outline_time"]
                    )
                    return redirect(
                        reverse("base:planer_initial", args=[_id])
                        + f"?page={page_obj.number + 1}&mode={str(mode)}"
                    )

        else:
            create_formset = create_formset()
            select_formset = select_formset()

        for form, target_lst in zip(select_formset.forms, page_obj):
            form.fields["choice"].choices = choices
            target_lst[0].form = form

        context = {
            "instance": instance,
            "outline_time": dict_time_obj_to_periods,
            "query": page_obj,
            "mode": str(mode),
            "formset": create_formset,
            "choice_formset": select_formset,
            "error": error,
        }

        return render(
            request,
            "base/new_outline/new_outline_initial_period2_1.html",
            context,
        )


@login_required
def initial_target(request, id1, id2):
    """ view with form for initial period outline detail """
    instance = get_object_or_404(
        models.Outline.objects.select_related(), id=id1, owner=request.user
    )
    if instance.written == "inactive":
        return Http404()

    target = get_object_or_404(models.TargetVertex, pk=id2)
    village_id = models.VillageModel.objects.get(
        world=instance.world, coord=target.target
    ).village_id

    link_to_tw = instance.world.tw_stats_link_to_village(village_id)

    result_lst = models.WeightModel.objects.filter(target=target).order_by("order")
    for weight in result_lst:
        weight.distance = round(weight.distance, 1)
    # sort
    sort_obj = basic.SortAndPaginRequest(
        outline=instance,
        GET_request=request.GET.get("sort"),
        PAGE_request=request.GET.get("page"),
        target=target,
    )
    page_obj = sort_obj.sorted_query()

    sort = sort_obj.sort
    # forms
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
                    + f"?page={page_obj.number}&sort={sort}"
                )

        if "form" in request.POST:
            form = forms.WeightForm(request.POST)
            if form.is_valid():
                weight_id = request.POST.get("weight_id")
                off = int(request.POST.get("off"))
                nobleman = int(request.POST.get("nobleman"))

                weight = models.WeightModel.objects.select_related("state").filter(
                    id=weight_id
                )[0]
                state = weight.state

                if off > weight.off:
                    state.off_max += off - weight.off

                if nobleman > weight.nobleman:
                    state.nobleman_max += nobleman - weight.nobleman

                state.off_state = state.off_state - weight.off + off
                state.nobleman_state = state.nobleman_state - weight.nobleman + nobleman

                state.off_left = state.off_max - state.off_state
                state.nobleman_left = state.nobleman_max - state.nobleman_state

                weight.off = off
                weight.nobleman = nobleman

                weight.save()
                state.save()
                return redirect(
                    reverse("base:planer_initial_detail", args=[id1, id2])
                    + f"?page={page_obj.number}&sort={sort}"
                )
        else:
            form = forms.WeightForm(None)

    else:
        form = forms.WeightForm(None)

    try:
        paint = int(request.session["weight"])
        del [request.session["weight"]]
    except KeyError:
        paint = None

    if paint is not None:
        for model in result_lst:
            if model.id == paint:
                model.paint = "paint"
                break
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
    }
    if target.fake:
        return render(
            request,
            "base/new_outline/new_outline_initial_period3_1.html",
            context,
        )
    else:
        return render(
            request,
            "base/new_outline/new_outline_initial_period3.html",
            context,
        )


@require_POST
@login_required
def initial_delete_time(request, pk):
    outline_time = get_object_or_404(models.OutlineTime.objects.select_related(), pk=pk)
    outline = get_object_or_404(
        models.Outline, owner=request.user, id=outline_time.outline.id
    )
    mode = request.GET.get("mode")
    page = request.GET.get("page")
    outline_time.delete()
    return redirect(
        reverse("base:planer_initial", args=[outline.id]) + f"?page={page}&mode={mode}"
    )

@require_POST
@login_required
def initial_set_all_time(request, pk):
    outline_time = get_object_or_404(models.OutlineTime.objects.select_related(), pk=pk)
    outline = get_object_or_404(
        models.Outline, owner=request.user, id=outline_time.outline.id
    )
    mode = request.GET.get("mode")
    page = request.GET.get("page")
    targets = models.TargetVertex.objects.filter(outline=outline)
    targets.update(outline_time=outline_time)

    return redirect(
        reverse("base:planer_initial", args=[outline.id]) + f"?page={page}&mode={mode}"
    )


@login_required
def create_final_outline(request, id1):
    instance = get_object_or_404(models.Outline.objects.select_related(), id=id1, owner=request.user)
    target_with_no_time = (
        models.TargetVertex.objects.filter(outline=instance)
        .filter(outline_time=None)
        .exists()
    )
    if target_with_no_time:
        request.session["outline_error"] = gettext("All targets must have Times")
        return redirect(
            reverse("base:planer_initial", args=[id1]) + "?page=1&mode=time"
        )
    models.Overview.objects.filter(outline=instance).update(removed=True)
    finish.make_final_outline(instance)
    return redirect("base:planer_detail_results", id1)


@login_required
def complete_outline(request, id1):
    instance = get_object_or_404(models.Outline.objects.select_related(), id=id1, owner=request.user)
    initial.complete_outline(outline=instance)
    instance.written = "active"
    instance.save()
    return redirect(reverse("base:planer_initial", args=[id1]) + "?page=1&mode=menu")


@login_required
def update_outline_troops(request, id1):
    instance = get_object_or_404(models.Outline.objects.select_related(), id=id1, owner=request.user)
    models.WeightMaximum.objects.filter(outline=instance).delete()
    off_form = forms.OffTroopsForm({"off_troops": instance.off_troops}, outline=instance)
    if off_form.is_valid():
        initial.make_outline(instance, make_targets=False)
    else:
        request.session["error"] = gettext("<h5>It looks like your Army collection is no longer actual!</h5> <p>To use the Planer:</p> <p>1. Paste the current data in the <b>Army collection</b> and <b>Submit</b>.</p> <p>2. Return to the <b>Planer</b> tab.</p> <p>3. Expand first tab <span class='md-correct2'>1. Available Troops</span>.</p> <p>4. Click the button <span class='md-correct2'>Click here to update if u have changed Army troops</span>.</p>")

        return redirect("base:planer_detail", id1)
    instance.avaiable_offs = []
    instance.avaiable_offs_near = []
    instance.avaiable_nobles = []
    instance.avaiable_nobles_near = []
    instance.save()
    return redirect("base:planer_initial_form", id1)
