from django.shortcuts import render, redirect

from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
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
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    if instance.off_troops == "":
        request.session["error"] = gettext("Off collection empty!")
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
        try:
            initial.make_outline(instance)
        except KeyError:
            request.session["error"] = gettext(
                (
                    "It looks like your Army collection is"
                    " no longer actual! "
                    "To use the planner: copy the data from"
                    " the preview and "
                    "correct errors or paste the current"
                    " military data \n"
                )
            )
            return redirect("base:planer_detail", _id)

    form1 = forms.InitialOutlineForm(None, world=instance.world)

    form2 = forms.AvailableTroopsForm(None)
    form3 = forms.SettingDateForm(None)
    form4 = forms.ModeOutlineForm(None)

    targets = models.TargetVertex.objects.filter(outline=instance).order_by("id")
    len_targets = len(targets)

    formset_select = formset_factory(
            form=forms.ModeTargetSetForm, extra=len_targets, max_num=len_targets
        )

    form1.fields["target"].initial = instance.initial_outline_targets
    form2.fields[
        "initial_outline_front_dist"
    ].initial = instance.initial_outline_front_dist
    form2.fields[
        "initial_outline_target_dist"
    ].initial = instance.initial_outline_target_dist
    form2.fields[
        "initial_outline_min_off"
    ].initial = instance.initial_outline_min_off
    form4.fields["mode_off"].initial = instance.mode_off
    form4.fields["mode_noble"].initial = instance.mode_noble
    form4.fields["mode_division"].initial = instance.mode_division
    form4.fields["mode_guide"].initial = instance.mode_guide
    form4.fields["initial_outline_fake_limit"].initial = instance.initial_outline_fake_limit


    

    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.InitialOutlineForm(request.POST, world=instance.world)
            if form1.is_valid():
                instance.initial_outline_targets = form1.clean_target()
                instance.save()
                # make outline
                try:
                    initial.make_outline(instance)
                except KeyError:
                    request.session["error"] = gettext(
                        (
                            "It looks like your Army collection is"
                            " no longer actual! "
                            "To use the planner: copy the data from"
                            " the preview and "
                            "correct errors or paste the current"
                            " military data \n"
                        )
                    )
                    return redirect("base:planer_detail", _id)

                instance.save()
                return redirect("base:planer_initial_form", _id)

        if "form2" in request.POST:
            form2 = forms.AvailableTroopsForm(request.POST)
            if form2.is_valid():
                min_off = request.POST.get("initial_outline_min_off")
                radius = request.POST.get("initial_outline_front_dist")
                radius_target = request.POST.get("initial_outline_target_dist")
                instance.initial_outline_min_off = min_off
                instance.initial_outline_front_dist = radius
                instance.initial_outline_target_dist = radius_target
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
                instance.mode_off = mode_off
                instance.mode_noble = mode_noble
                instance.mode_division = mode_division
                instance.mode_guide = mode_guide
                instance.initial_outline_fake_limit = fake_limit
                instance.save()

                models.TargetVertex.objects.filter(outline=instance).update(mode_off=mode_off, mode_noble=mode_noble, mode_division=mode_division, mode_guide=mode_guide)
                models.WeightMaximum.objects.filter(outline=instance).update(fake_limit=fake_limit)

                return redirect("base:planer_initial_form", _id)
        
        if "formset" in request.POST:
            formset_select = formset_select(request.POST)
            if formset_select.is_valid():
                targets_to_update = []
                for data, target in zip(formset_select.cleaned_data, targets):
                    target.mode_off = data['mode_off']
                    target.mode_noble = data['mode_noble']
                    target.mode_division = data['mode_division']
                    target.mode_guide = data['mode_guide']
                    targets_to_update.append(target)
                models.TargetVertex.objects.bulk_update(targets_to_update, fields=['mode_off', 'mode_noble', 'mode_division', 'mode_guide', ])
                return redirect("base:planer_initial_form", _id)
        else:
            formset_select = formset_select(None)
    else:
        formset_select = formset_select(None)

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
        "formset": formset_select,
    }
    return render(
        request, "base/new_outline/new_outline_initial_period1.html", context
    )


@login_required
def initial_planer(request, _id):
    """ view with form for initial period outline """
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
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
                    x_coord = coord[0:3]
                    y_coord = coord[4:7]
                    village_id = x_coord + y_coord + str(instance.world)

                    village = models.VillageModel.objects.get(pk=village_id)
                    player = models.Player.objects.get(
                        player_id=village.player_id, world=instance.world
                    )

                    models.TargetVertex.objects.create(
                        outline=instance,
                        player=player.name,
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
            (f"{time.order}", f"{time.order}")
            for time in dict_time_obj_to_periods
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
                            outline_times_Q.aggregate(Max("order"))[
                                "order__max"
                            ]
                            + 1
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
                            form.fields[err].widget.attrs[
                                "class"
                            ] += " border-invalid"

            if "choice-formset" in request.POST:
                select_formset = select_formset(request.POST)
                for form in select_formset.forms:
                    form.fields["choice"].choices = choices
                create_formset = create_formset()
                if select_formset.is_valid():
                    update_list = []
                    for data, tup in zip(
                        select_formset.cleaned_data, page_obj
                    ):
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
    instance = get_object_or_404(models.Outline, id=id1, owner=request.user)
    if instance.written == "inactive":
        return Http404()

    target = get_object_or_404(models.TargetVertex, pk=id2)
    x = int(target.target[0:3])
    y = int(target.target[4:7])
    world = models.World.objects.get(world=instance.world)
    village_id = models.VillageModel.objects.get(world=world.world, x_coord=x, y_coord=y).village_id

    link_to_tw = world.tw_stats_link_to_village(village_id)

    result_lst = models.WeightModel.objects.filter(target=target).order_by(
        "order"
    )
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

                weight = models.WeightModel.objects.select_related(
                    "state"
                ).filter(id=weight_id)[0]
                state = weight.state

                if off > weight.off:
                    state.off_max += off - weight.off

                if nobleman > weight.nobleman:
                    state.nobleman_max += nobleman - weight.nobleman

                state.off_state = state.off_state - weight.off + off
                state.nobleman_state = (
                    state.nobleman_state - weight.nobleman + nobleman
                )

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


class InitialDeleteTime(LoginRequiredMixin, DeleteView):
    model = models.OutlineTime

    def get_success_url(self):
        outline = self.object.outline
        mode = self.request.GET.get("mode")
        page = self.request.GET.get("page")
        return (
            reverse("base:planer_initial", args=[outline.id])
            + f"?page={page}&mode={mode}"
        )


@login_required
def create_final_outline(request, id1):
    instance = get_object_or_404(models.Outline, id=id1, owner=request.user)
    target_with_no_time = (
        models.TargetVertex.objects.filter(outline=instance)
        .filter(outline_time=None)
        .exists()
    )
    if target_with_no_time:
        request.session["outline_error"] = gettext(
            "All targets must have Times"
        )
        return redirect(
            reverse("base:planer_initial", args=[id1]) + "?page=1&mode=time"
        )
    models.Overview.objects.filter(outline=instance).delete()
    finish.make_final_outline(instance)
    return redirect("base:planer_detail_results", id1)


@login_required
def complete_outline(request, id1):
    instance = get_object_or_404(models.Outline, id=id1, owner=request.user)
    initial.complete_outline(outline=instance)
    instance.written = "active"
    instance.save()
    return redirect(
        reverse("base:planer_initial", args=[id1]) + "?page=1&mode=menu"
    )


@login_required
def update_outline_troops(request, id1):
    instance = get_object_or_404(models.Outline, id=id1, owner=request.user)
    models.WeightMaximum.objects.all().delete()
    try:
        initial.make_outline(instance)
    except KeyError:
        request.session["error"] = gettext(
            (
                "It looks like your Army collection is"
                " no longer actual! "
                "To use the planner: copy the data from"
                " the preview and "
                "correct errors or paste the current"
                " military data \n"
            )
        )
        return redirect("base:planer_detail", id1)

    instance.save()
    return redirect("base:planer_initial_form", id1)
