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

from time import time

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext
from django.views.decorators.http import require_POST

from base import forms, models
from base.models.profile import Profile
from utils.basic import Troops


def get_show_hidden(request: HttpRequest) -> bool:
    match request.GET.get("show-hidden"):
        case "true":
            return True
        case _:
            return False


@login_required
def outline_list(request: HttpRequest) -> HttpResponse:
    show_hidden = get_show_hidden(request)

    models.Outline.objects.filter(editable="active", owner=request.user).delete()

    outlines = (
        models.Outline.objects.select_related("world", "world__server")
        .filter(owner=request.user)
        .annotate(parent_outline_name=F("parent_outline__name"))
    )
    if not show_hidden:
        outlines = outlines.filter(status="active")

    for outline in outlines:
        # overwrite attributes
        setattr(outline, "world_human", outline.world.game_name(prefix=True))
        setattr(outline, "ally_tribe_tag", ", ".join(outline.ally_tribe_tag))
        setattr(outline, "enemy_tribe_tag", ", ".join(outline.enemy_tribe_tag))
        setattr(
            outline,
            "duplicate_form",
            forms.OutlineDuplicateForm(
                initial={
                    "unused_troops": True,
                    "parent_outline": outline,
                    "date": outline.date,
                }
            ),
        )

    form1 = forms.OutlineDuplicateForm(None)

    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.OutlineDuplicateForm(request.POST)
            if form1.is_valid():
                instance: models.Outline = form1.save(commit=False)
                old_outline = get_object_or_404(
                    models.Outline, id=instance.parent_outline_id, owner=request.user
                )
                old_result: models.Result = old_outline.result  # type: ignore
                unused_troops = request.POST.get("unused_troops") == "on"
                with transaction.atomic():
                    old_outline.actions.outline_duplicated(old_outline)
                    new_outline = old_outline
                    new_outline.pk = None
                    new_outline.name = instance.name
                    new_outline.date = instance.date
                    new_outline.parent_outline_id = instance.parent_outline_id
                    new_outline.off_troops = ""
                    new_outline.off_troops_hash = ""
                    new_outline.off_troops_weightmodels_hash = ""
                    new_outline.deff_troops = ""
                    new_outline.deff_troops_hash = ""
                    new_outline.deff_troops_weightmodels_hash = ""
                    new_outline.save()
                    if unused_troops and old_result.results_export:
                        if old_outline.input_data_type == old_outline.ARMY_COLLECTION:
                            new_outline.off_troops = old_result.results_export
                            new_outline.save(update_fields=["off_troops"])
                            new_outline.get_or_set_off_troops_hash(
                                force_recalculate=True
                            )
                        else:
                            new_outline.deff_troops = old_result.results_export
                            new_outline.save(update_fields=["deff_troops"])
                            new_outline.get_or_set_deff_troops_hash(
                                force_recalculate=True
                            )

                    result = models.Result(outline=new_outline)
                    result.save()
                    new_outline.create_stats()

                    new_outline.remove_user_outline()

                    new_outline.initial_outline_targets = ""
                    new_outline.initial_outline_fakes = ""
                    new_outline.initial_outline_ruins = ""
                    new_outline.save(
                        update_fields=[
                            "initial_outline_targets",
                            "initial_outline_fakes",
                            "initial_outline_ruins",
                        ]
                    )

                return redirect(
                    reverse("base:planer") + f"?show-hidden={str(show_hidden).lower()}"
                )
            for outline in outlines:
                if request.POST.get("parent_outline") == str(outline.pk):
                    setattr(
                        outline,
                        "duplicate_form",
                        form1,
                    )
                    break

    context = {"form1": form1, "show_hidden": show_hidden, "outlines": outlines}
    return render(request, "base/base_planer.html", context)


@login_required
@require_POST
def inactive_outline(request: HttpRequest, _id: int) -> HttpResponse:
    """class based view makeing outline with id=id inavtive/active, post and login required"""

    outline = get_object_or_404(models.Outline, id=_id, owner=request.user)
    show_hidden = get_show_hidden(request)

    if outline.status == "active":
        outline.status = "inactive"
        outline.save(update_fields=["status"])
    else:
        outline.status = "active"
        outline.save(update_fields=["status"])

    return redirect(reverse("base:planer") + f"?show-hidden={str(show_hidden).lower()}")


@login_required
@require_POST
def outline_delete(request: HttpRequest, _id: int) -> HttpResponse:
    outline = get_object_or_404(models.Outline, id=_id, owner=request.user)
    show_hidden = get_show_hidden(request)

    outline.delete()
    return redirect(reverse("base:planer") + f"?show-hidden={str(show_hidden).lower()}")


@login_required
def outline_detail(request: HttpRequest, _id: int) -> HttpResponse:  # noqa: PLR0912
    """details user's outline , login required"""
    models.Outline.objects.filter(editable="active", owner=request.user).delete()
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )
    form_input_type = forms.InputDataPlanerForm(None, instance=instance)
    form1 = forms.OffTroopsForm(None, outline=instance)
    form2 = forms.DeffTroopsForm(None, outline=instance)

    off_troops = Troops(instance, "off_troops")
    deff_troops = Troops(instance, "deff_troops")

    if request.method == "POST":
        if "form-input" in request.POST:
            form_input_type = forms.InputDataPlanerForm(request.POST, instance=instance)
            if form_input_type.is_valid():
                form_input_type.save()
                set_as_default: bool = form_input_type.cleaned_data["set_as_default"]
                if set_as_default:
                    profile: Profile = request.user.profile  # type: ignore
                    profile.input_data_type = form_input_type.cleaned_data[
                        "input_data_type"
                    ]
                    profile.save()
                return redirect("base:planer_detail", _id)

        if "form-1" in request.POST:
            form10 = forms.OffTroopsForm(request.POST, outline=instance)
            instance.actions.save_off_troops(instance)
            if form10.is_valid():
                instance.off_troops = request.POST["off_troops"]
                instance.off_troops_hash = instance.get_or_set_off_troops_hash(
                    force_recalculate=True
                )
                instance.save(update_fields=["off_troops", "off_troops_hash"])
                request.session["message-off-troops"] = "true"
                return redirect("base:planer_detail", _id)
            else:
                off_troops.set_troops(request.POST.get("off_troops"))
                off_troops.set_errors(form10.errors)
                off_troops.set_first_error_msg(form10.first_error_message)
                off_troops.set_second_error_msg(form10.second_error_message)

        elif "form-2" in request.POST:
            form20 = forms.DeffTroopsForm(request.POST, outline=instance)
            instance.actions.save_deff_troops(instance)
            if form20.is_valid():
                instance.deff_troops = request.POST["deff_troops"]
                instance.deff_troops_hash = instance.get_or_set_deff_troops_hash(
                    force_recalculate=True
                )
                instance.save(update_fields=["deff_troops", "deff_troops_hash"])
                request.session["message-deff-troops"] = "true"
                return redirect("base:planer_detail", _id)
            else:
                deff_troops.set_troops(request.POST.get("deff_troops"))
                deff_troops.set_errors(form20.errors)
                deff_troops.set_first_error_msg(form20.first_error_message)
                deff_troops.set_second_error_msg(form20.second_error_message)

    if instance.world.postfix == "Test":
        setattr(instance.world, "update", gettext("Never") + ".")
    else:
        _timedelta = time() - instance.world.last_modified_timestamp()
        setattr(
            instance.world,
            "update",
            str(round(_timedelta / 60)) + gettext(" minute(s) ago."),
        )

    context = {
        "instance": instance,
        "form1": form1,
        "off_troops": off_troops,
        "deff_troops": deff_troops,
        "form2": form2,
        "form_input_type": form_input_type,
    }
    message_off = request.session.get("message-off-troops")
    if message_off is not None:
        context["message_off"] = message_off
        del request.session["message-off-troops"]

    message_deff = request.session.get("message-deff-troops")
    if message_deff is not None:
        context["message_deff"] = message_deff
        del request.session["message-deff-troops"]

    error = request.session.get("error")
    if error is not None:
        context["error"] = error
        del request.session["error"]
    return render(request, "base/new_outline/new_outline.html", context)
