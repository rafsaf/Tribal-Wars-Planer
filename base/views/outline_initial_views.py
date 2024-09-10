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

import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.db.models import Max
from django.forms import formset_factory
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext
from django.views.decorators.http import require_POST

import metrics
from base import forms, models
from base.models.target_vertex import TargetVertex
from utils import avaiable_troops, basic
from utils.outline_complete import complete_outline_write
from utils.outline_create_targets import OutlineCreateTargets
from utils.outline_finish import MakeFinalOutline
from utils.outline_initial import MakeOutline

log = logging.getLogger(__name__)


def trigger_off_troops_update_redirect(
    request: HttpRequest, outline: models.Outline
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    request.session["error"] = gettext(
        "<h5>It looks like your %(collection)s is no longer actual!</h5> "
        "<p>To use the Planer:</p> "
        "<p>1. Paste the current data in the <b>%(collection)s</b>, solve issues.</p> "
        "<p>2. Click on <b>Submit</b>.</p> "
        "<p>3. Only then return to the <b>Planer</b> tab.</p> "
    ) % {"collection": outline.get_input_data_trans()}

    return redirect("base:planer_detail", outline.pk)


def outline_being_written_error(
    instance: models.Outline, request: HttpRequest, lock: models.OutlineWriteLock
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    now = timezone.now()
    log.warning("complete_outline locked outline %s", instance.pk)
    metrics.ERRORS.labels("complete_outline_locked_outline").inc()
    request.session["error"] = gettext(
        "<h5>It looks like your outline in being written just now!</h5> "
        '<p>You cannot click on "Write an outline" button more than once at the same time.</p> '
        "<p>Try to refresh this page in a moment. The lock force expires in <b>%(lock_expire)ss</b>.</p> "
    ) % {"lock_expire": (lock.lock_expire - now).seconds}
    target_mode: str | None = request.GET.get("t")
    return redirect(
        reverse("base:planer_initial_form", args=[instance.pk]) + f"?t={target_mode}"
    )


def outline_onging_weightmax_creating_error(
    instance: models.Outline, request: HttpRequest, lock: models.OutlineWriteLock
) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    now = timezone.now()
    log.warning("make_outline locked outline %s", instance.pk)
    metrics.ERRORS.labels("make_outline_locked_outline").inc()
    request.session["error"] = gettext(
        "<h5>It looks like your outline in being changed just now!</h5> "
        "<p>Data about villages is being created or recreated.</p> "
        "<p>Try to refresh this page in a moment. The lock force expires in <b>%(lock_expire)ss</b>.</p> "
    ) % {"lock_expire": (lock.lock_expire - now).seconds}
    target_mode: str | None = request.GET.get("t")
    return redirect(
        reverse("base:planer_initial_form", args=[instance.pk]) + f"?t={target_mode}"
    )


@login_required
def initial_form(  # noqa: PLR0912,PLR0911
    request: HttpRequest, _id: int
) -> HttpResponse:
    """
    view with table with created outline,

    returned after valid filled form earlier

    """
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )
    now = timezone.now()
    if (
        instance.input_data_type == models.Outline.ARMY_COLLECTION
        and instance.off_troops == ""
    ):
        request.session["error"] = gettext("<h5>Army collection is empty!</h5>")
        return redirect("base:planer_detail", _id)
    elif (
        instance.input_data_type == models.Outline.DEFF_COLLECTION
        and instance.deff_troops == ""
    ):
        request.session["error"] = gettext("<h5>Deff collection is empty!</h5>")
        return redirect("base:planer_detail", _id)

    if instance.written == "active":
        return redirect("base:planer_initial", _id)
    premium_error: bool
    if request.session.get("premium_error") is True:
        premium_error = True
        del request.session["premium_error"]
    else:
        premium_error = False
    error = request.session.get("error")

    if error is not None:
        pass
    elif instance.input_data_type == models.Outline.ARMY_COLLECTION:
        if (
            models.WeightMaximum.objects.filter(outline=instance).count() == 0
            or instance.get_or_set_off_troops_hash()
            != instance.off_troops_weightmodels_hash
        ):
            current_lock = models.OutlineWriteLock.objects.filter(
                outline_id=instance.pk,
                lock_name=models.OutlineWriteLock.LOCK_NAME_TYPES.CREATE_WEIGHTMAX,
                lock_expire__gt=now,
            ).first()
            if current_lock:
                return outline_onging_weightmax_creating_error(
                    instance, request, current_lock
                )

            off_form = forms.OffTroopsForm(
                {"off_troops": instance.off_troops}, outline=instance
            )
            if off_form.is_valid():
                # remove old locks
                models.OutlineWriteLock.objects.filter(
                    outline_id=instance.pk,
                    lock_expire__lt=now,
                ).delete()

                lock, created = models.OutlineWriteLock.objects.get_or_create(
                    outline_id=instance.pk,
                    lock_name=models.OutlineWriteLock.LOCK_NAME_TYPES.CREATE_WEIGHTMAX,
                    defaults={"lock_expire": now + timedelta(seconds=70)},
                )
                if not created:
                    return outline_onging_weightmax_creating_error(
                        instance, request, lock
                    )

                try:
                    with transaction.atomic():
                        make_outline = MakeOutline(outline=instance)
                        make_outline()

                    instance.actions.click_troops_refresh(instance)
                finally:
                    lock.delete()
            else:
                return trigger_off_troops_update_redirect(
                    request=request, outline=instance
                )
    elif (
        models.WeightMaximum.objects.filter(outline=instance).count() == 0
        or instance.get_or_set_deff_troops_hash()
        != instance.deff_troops_weightmodels_hash
    ):
        current_lock = models.OutlineWriteLock.objects.filter(
            outline_id=instance.pk,
            lock_name=models.OutlineWriteLock.LOCK_NAME_TYPES.CREATE_WEIGHTMAX,
            lock_expire__gt=now,
        ).first()
        if current_lock:
            return outline_onging_weightmax_creating_error(
                instance, request, current_lock
            )

        deff_form = forms.DeffTroopsForm(
            {"deff_troops": instance.deff_troops}, outline=instance
        )
        if deff_form.is_valid():
            # remove old locks
            models.OutlineWriteLock.objects.filter(
                outline_id=instance.pk,
                lock_expire__lt=now,
            ).delete()

            lock, created = models.OutlineWriteLock.objects.get_or_create(
                outline_id=instance.pk,
                lock_name=models.OutlineWriteLock.LOCK_NAME_TYPES.CREATE_WEIGHTMAX,
                defaults={"lock_expire": now + timedelta(seconds=70)},
            )
            if not created:
                return outline_onging_weightmax_creating_error(instance, request, lock)

            try:
                with transaction.atomic():
                    make_outline = MakeOutline(outline=instance)
                    make_outline()

                instance.actions.click_troops_refresh(instance)
            finally:
                lock.delete()
        else:
            return trigger_off_troops_update_redirect(request=request, outline=instance)

    target_mode = basic.TargetMode(request.GET.get("t"))

    form1 = forms.InitialOutlineForm(None, outline=instance, target_mode=target_mode)
    form2 = forms.AvailableTroopsForm(None, instance=instance)
    form3 = forms.SettingDateForm(None)
    form3.fields["date"].initial = instance.date.strftime("%Y-%m-%d")
    form4 = forms.ModeOutlineForm(None, instance=instance)
    form5 = forms.NightBonusSetForm(None, instance=instance)
    form6 = forms.RuiningOutlineForm(None, instance=instance)
    form7 = forms.MoraleOutlineForm(None, instance=instance)

    calc: basic.TargetsCalculations = basic.TargetsCalculations(
        outline=instance, target_mode=target_mode
    )
    estimated_time = 10 * (calc.len_real + calc.len_fake) + 18 * calc.len_ruin

    if instance.morale_on and instance.world.morale > 0:
        morale_dict = basic.generate_morale_dict(instance)
    else:
        morale_dict = None

    if target_mode.is_real:
        form1.fields["target"].initial = instance.initial_outline_targets
    elif target_mode.is_fake:
        form1.fields["target"].initial = instance.initial_outline_fakes
    else:
        form1.fields["target"].initial = instance.initial_outline_ruins

    if request.method == "POST":
        lock = models.OutlineWriteLock.objects.filter(
            outline_id=instance.pk,
            lock_name=models.OutlineWriteLock.LOCK_NAME_TYPES.WRITE_OUTLINE,
            lock_expire__gt=now,
        ).first()
        if lock:
            return outline_being_written_error(instance, request, lock)
        if "form1" in request.POST:
            max_to_add = (
                settings.INPUT_OUTLINE_MAX_TARGETS
                - calc.len_fake
                - calc.len_real
                - calc.len_ruin
                + calc.actual_len
            )
            form1 = forms.InitialOutlineForm(
                request.POST,
                outline=instance,
                target_mode=target_mode,
                max_to_add=max_to_add,
            )
            if form1.is_valid():
                if instance.input_data_type == models.Outline.ARMY_COLLECTION:
                    off_form = forms.OffTroopsForm(
                        {"off_troops": instance.off_troops}, outline=instance
                    )
                    if not off_form.is_valid():
                        return trigger_off_troops_update_redirect(
                            request=request, outline=instance
                        )
                else:
                    deff_form = forms.DeffTroopsForm(
                        {"deff_troops": instance.deff_troops}, outline=instance
                    )
                    if not deff_form.is_valid():
                        return trigger_off_troops_update_redirect(
                            request=request, outline=instance
                        )

                instance.save()
                create_targets = OutlineCreateTargets(instance, target_mode)
                create_targets()
                if target_mode.is_real:
                    instance.actions.save_real_targets(instance)
                elif target_mode.is_fake:
                    instance.actions.save_fake_targets(instance)
                else:
                    instance.actions.save_ruin_targets(instance)

                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form2" in request.POST:
            form2 = forms.AvailableTroopsForm(request.POST, instance=instance)
            if form2.is_valid():
                instance.actions.form_available_troops(instance)
                form2.save()
                instance.refresh_from_db()
                avaiable_troops.get_legal_coords_outline(outline=instance)
                avaiable_troops.update_available_ruins(outline=instance)
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form3" in request.POST:
            form3 = forms.SettingDateForm(request.POST, instance=instance)
            if form3.is_valid():
                instance.actions.form_date_change(instance)
                form3.save()
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form4" in request.POST:
            form4 = forms.ModeOutlineForm(request.POST, instance=instance)
            if form4.is_valid():
                instance.actions.form_settings_change(instance)
                form4.save()
                instance.refresh_from_db()
                models.TargetVertex.objects.filter(outline=instance).update(
                    mode_off=instance.mode_off,
                    mode_noble=instance.mode_noble,
                    mode_division=instance.mode_division,
                    mode_guide=instance.mode_guide,
                )
                models.WeightMaximum.objects.filter(outline=instance).update(
                    fake_limit=instance.initial_outline_fake_limit,
                    nobles_limit=instance.initial_outline_nobles_limit,
                )

                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form5" in request.POST:
            form5 = forms.NightBonusSetForm(request.POST, instance=instance)
            if form5.is_valid():
                instance.actions.form_night_change(instance)
                form5.save()
                instance.refresh_from_db()
                models.TargetVertex.objects.filter(outline=instance).update(
                    night_bonus=instance.night_bonus,
                    enter_t1=instance.enter_t1,
                    enter_t2=instance.enter_t2,
                )
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form6" in request.POST:
            form6 = forms.RuiningOutlineForm(request.POST, instance=instance)
            if form6.is_valid():
                instance.actions.form_ruin_change(instance)
                form6.save()
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

        if "form7" in request.POST:
            form7 = forms.MoraleOutlineForm(request.POST, instance=instance)
            if form7.is_valid():
                instance = form7.save(commit=False)
                instance.save()
                return redirect(
                    reverse("base:planer_initial_form", args=[_id])
                    + f"?t={target_mode.mode}"
                )

    if not instance.avaiable_offs:
        avaiable_troops.get_legal_coords_outline(outline=instance)
        avaiable_troops.update_available_ruins(outline=instance)

    context = {
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,
        "form5": form5,
        "form6": form6,
        "form7": form7,
        "calc": calc,
        "mode": target_mode.mode,
        "morale_dict": morale_dict.items() if morale_dict else None,
        "estimated_time": estimated_time,
        "premium_error": premium_error,
        "premium_account_max_targets_free": settings.PREMIUM_ACCOUNT_MAX_TARGETS_FREE,
    }
    if error is not None:
        context["error"] = error
        del request.session["error"]
    return render(request, "base/new_outline/new_outline_initial_period1.html", context)


@login_required
def initial_planer(  # noqa: PLR0912,PLR0911
    request: HttpRequest, _id: int
) -> HttpResponse:
    """view with form for initial period outline"""
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )
    if instance.written == "inactive":
        raise Http404()
    profile: models.Profile = request.user.profile  # type: ignore
    is_premium: bool = profile.is_premium()
    filter_form = forms.SetTargetsMenuFilters(None)
    filter_form.fields["filter_targets_number"].initial = instance.filter_targets_number
    filter_form.fields["simple_textures"].initial = instance.simple_textures
    target_form = forms.CreateNewInitialTarget(
        None, outline=instance, is_premium=is_premium
    )
    mode: basic.Mode = basic.Mode(request.GET.get("mode"))
    page_number = request.GET.get("page")
    filtr = request.GET.get("filtr") or ""

    if request.method == "POST":
        if "form1" in request.POST:
            instance.actions.click_go_back(instance)
            instance.remove_user_outline()
            return redirect("base:planer_initial_form", _id)

        if "form-filter-targets" in request.POST:
            filter_form = forms.SetTargetsMenuFilters(request.POST)
            if filter_form.is_valid():
                cards = int(request.POST["filter_targets_number"])
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
            message: str | None = request.session.get("success")
            if message is not None:
                del request.session["success"]

            context["target_form"] = target_form
            context["message"] = message

        return render(
            request,
            "base/new_outline/new_outline_initial_period2.html",
            context,
        )

    error: str | None = request.session.get("outline_error")
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
    outline_time_dict = instance.get_outline_times()

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
            elif not models.OutlineTime.objects.filter(outline=instance).exists():
                request.session["outline_error"] = gettext(
                    "<h5>Minimum one Time must exists.</h5>"
                )
                return redirect(
                    reverse("base:planer_initial", args=[_id]) + "?page=1&mode=time"
                )
            models.Overview.objects.filter(outline=instance).update(removed=True)
            make_final_outline = MakeFinalOutline(instance)

            error_messages = make_final_outline()
            if len(error_messages) > 0:
                request.session["error_messages"] = ",".join(error_messages)
            instance.actions.click_outline_finish(instance)

            return redirect("base:planer_detail_results", _id)

        if "formset" in request.POST:
            create_formset = create_formset(request.POST)
            select_formset = select_formset()
            if create_formset.is_valid():
                instance.actions.save_time_created(instance)
                outline_times_Q = models.OutlineTime.objects.filter(outline=instance)
                if outline_times_Q.count() == 0:
                    order = 1
                else:
                    order = outline_times_Q.aggregate(Max("order"))["order__max"] + 1

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
def initial_target(  # noqa: PLR0912
    request: HttpRequest, id1: int, id2: int
) -> HttpResponse:
    """view with form for initial period outline detail"""
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=id1, owner=request.user
    )
    if instance.written == "inactive":
        raise Http404()

    target = get_object_or_404(models.TargetVertex, pk=id2)
    try:
        village_id = models.VillageModel.objects.get(
            world=instance.world, coord=target.target
        ).village_id
    except models.VillageModel.DoesNotExist:
        raise Http404()

    link_to_tw = instance.world.tw_stats_link_to_village(village_id)

    result_lst = (
        models.WeightModel.objects.select_related("state")
        .filter(target=target)
        .order_by("order")
    )
    for weight_obj in result_lst:
        weight_obj.distance = round(weight_obj.distance, 1)
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
    filter_form = forms.SetNewOutlineFilters(request.POST or None, instance=instance)

    if request.method == "POST":
        if "form-filter" in request.POST:
            if filter_form.is_valid():
                filter_form.save()
                return redirect(
                    reverse("base:planer_initial_detail", args=[id1, id2])
                    + f"?page={page_obj.number}&sort={sort}&filtr={filtr}"  # type: ignore
                )

        if "form" in request.POST:
            form = forms.WeightForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    weight_id: str | None = request.POST.get("weight_id")
                    off_no_cats_post: str | None = request.POST.get("off_no_catapult")
                    nobleman_post: str | None = request.POST.get("nobleman")
                    catapult_post: str | None = request.POST.get("catapult")

                    weight: models.WeightModel = get_object_or_404(
                        models.WeightModel.objects.select_for_update().select_related(
                            "state"
                        ),
                        pk=weight_id,
                    )
                    state = weight.state
                    if (
                        nobleman_post is None
                        or off_no_cats_post is None
                        or catapult_post is None
                    ):
                        raise Http404()

                    nobleman = int(nobleman_post)
                    off_no_cats = int(off_no_cats_post)
                    catapult = int(catapult_post)

                    off_diffrence: int = off_no_cats + catapult * 8 - weight.off
                    noble_diffrence: int = nobleman - weight.nobleman
                    catapult_diffrence: int = catapult - weight.catapult

                    if not all(
                        [
                            noble_diffrence <= state.nobleman_left,
                            -weight.nobleman <= noble_diffrence,
                            off_diffrence <= state.off_left,
                            -weight.off <= off_diffrence,
                            catapult_diffrence <= state.catapult_left,
                            -weight.catapult <= catapult_diffrence,
                        ]
                    ):
                        raise Http404()

                    state.off_state += off_diffrence
                    state.off_left -= off_diffrence
                    state.nobleman_state += noble_diffrence
                    state.nobleman_left -= noble_diffrence
                    state.catapult_state += catapult_diffrence
                    state.catapult_left -= catapult_diffrence

                    weight.off += off_diffrence
                    weight.nobleman += noble_diffrence
                    weight.catapult += catapult_diffrence

                    weight.save()
                    state.save()
                    return redirect(
                        reverse("base:planer_initial_detail", args=[id1, id2])
                        + f"?page={page_obj.number}&sort={sort}&filtr={filtr}"  # type: ignore
                    )
        else:
            form = forms.WeightForm(None)

    else:
        form = forms.WeightForm(None)

    paint: str | None = request.session.get("weight")
    if paint is not None:
        try:
            paint_id: int = int(paint)
        except ValueError:
            pass
        else:
            for model in result_lst:
                if model.pk == paint_id:
                    setattr(model, "paint", "paint")
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


@login_required
@require_POST
def initial_delete_time(request: HttpRequest, pk: int) -> HttpResponse:
    outline_time: models.OutlineTime = get_object_or_404(
        models.OutlineTime.objects.select_related(), pk=pk
    )
    outline: models.Outline = get_object_or_404(
        models.Outline, owner=request.user, id=outline_time.outline.pk
    )
    mode: str | None = request.GET.get("mode")
    page: str | None = request.GET.get("page")
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
        models.Outline, owner=request.user, id=outline_time.outline.pk
    )
    mode: str | None = request.GET.get("mode")
    page: str | None = request.GET.get("page")
    fake: str | None = request.GET.get("fake")
    ruin: str | None = request.GET.get("ruin")

    fake_state: bool = False
    ruin_state: bool = False
    if fake == "true":
        fake_state = True
        outline.default_fake_time_id = outline_time.pk
    elif ruin == "true":
        ruin_state = True
        outline.default_ruin_time_id = outline_time.pk
    else:
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
def initial_set_all_time_page(request: HttpRequest, pk: int) -> HttpResponse:
    outline_time: models.OutlineTime = get_object_or_404(
        models.OutlineTime.objects.select_related(), pk=pk
    )
    outline: models.Outline = get_object_or_404(
        models.Outline, owner=request.user, id=outline_time.outline.pk
    )
    mode = request.GET.get("mode")
    page = request.GET.get("page")
    filtr = request.GET.get("filtr") or ""

    page_obj = outline.pagin_targets(
        page=page,
        every=True,
        not_empty_only=True,
        related=True,
        filtr=filtr,
    )

    TargetVertex.objects.filter(
        outline=outline, id__in=[target.pk for target in page_obj]
    ).update(outline_time=outline_time)

    return redirect(
        reverse("base:planer_initial", args=[outline.pk])
        + f"?page={page}&mode={mode}&filtr={filtr}"
    )


@login_required
@require_POST
def complete_outline(request: HttpRequest, id1: int) -> HttpResponse:
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=id1, owner=request.user
    )
    if instance.written == "active":
        return redirect("base:planer_initial", id1)
    user: AbstractBaseUser | AnonymousUser = request.user
    profile: models.Profile = models.Profile.objects.get(user=user)
    if not profile.is_premium():
        target_mode: str | None = request.GET.get("t")
        target_count: int = models.TargetVertex.objects.filter(outline=instance).count()
        if target_count > settings.PREMIUM_ACCOUNT_MAX_TARGETS_FREE:
            request.session["premium_error"] = True
            return redirect(
                reverse("base:planer_initial_form", args=[id1]) + f"?t={target_mode}"
            )
    # delete old lock
    now = timezone.now()
    models.OutlineWriteLock.objects.filter(
        outline_id=instance.pk,
        lock_expire__lt=now,
    ).delete()
    # try acquire lock on outline for 120s or result in error
    lock, created = models.OutlineWriteLock.objects.get_or_create(
        outline_id=instance.pk,
        lock_name=models.OutlineWriteLock.LOCK_NAME_TYPES.WRITE_OUTLINE,
        defaults={"lock_expire": now + timedelta(seconds=600)},
    )
    if not created:
        return outline_being_written_error(instance, request, lock)
    try:
        with transaction.atomic():
            complete_outline_write(outline=instance)
            instance.actions.click_outline_write(instance)
            instance.written = "active"
            instance.save()
    except Exception as err:
        log.error("outline_complete_write unknown error: %s", err, exc_info=True)
        metrics.ERRORS.labels("complete_outline_unkown_error").inc()

        lock.delete()
        raise

    lock.delete()
    return redirect(reverse("base:planer_initial", args=[id1]) + "?page=1&mode=menu")
