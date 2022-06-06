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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from base import forms, models
from base.views.outline_initial_views import trigger_off_deff_troops_update_redirect
from utils.basic import Troops
from utils.outline_troops_analysis import OutlineTroopsAnalysis


class OutlineList(LoginRequiredMixin, ListView):
    """login required view /planer"""

    template_name = "base/base_planer.html"

    def get_queryset(self):
        models.Outline.objects.filter(
            editable="active", owner=self.request.user
        ).delete()
        query = (
            models.Outline.objects.select_related("world")
            .filter(owner=self.request.user)
            .filter(status="active")
        )

        for outline in query:
            # overwrite attributes
            setattr(outline, "world_human", outline.world.human(prefix=True))
            setattr(outline, "ally_tribe_tag", ", ".join(outline.ally_tribe_tag))
            setattr(outline, "enemy_tribe_tag", ", ".join(outline.enemy_tribe_tag))

        return query


class OutlineListShowAll(LoginRequiredMixin, ListView):
    """login required view which shows hidden instances /planer/show_all"""

    template_name = "base/base_planer.html"

    def get_queryset(self):
        models.Outline.objects.filter(
            editable="active", owner=self.request.user
        ).delete()
        query = models.Outline.objects.select_related("world").filter(
            owner=self.request.user
        )

        for outline in query:
            # overwrite attributes
            setattr(outline, "world_human", outline.world.human(prefix=True))
            setattr(outline, "ally_tribe_tag", ", ".join(outline.ally_tribe_tag))
            setattr(outline, "enemy_tribe_tag", ", ".join(outline.enemy_tribe_tag))

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_all"] = True
        return context


@login_required
@require_POST
def inactive_outline(request: HttpRequest, _id: int) -> HttpResponse:
    """class based view makeing outline with id=id inavtive/active, post and login required"""

    outline = get_object_or_404(models.Outline, id=_id, owner=request.user)
    if outline.status == "active":
        outline.status = "inactive"
        outline.save()
        return redirect("base:planer")
    else:
        outline.status = "active"
        outline.save()
        return redirect("base:planer_all")


@login_required
@require_POST
def outline_delete(request: HttpRequest, _id: int) -> HttpResponse:
    outline = get_object_or_404(models.Outline, id=_id, owner=request.user)
    outline.delete()
    return redirect("base:planer")


@login_required
def outline_detail(request: HttpRequest, _id: int) -> HttpResponse:
    """details user's outline , login required"""
    models.Outline.objects.filter(editable="active", owner=request.user).delete()
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )

    form1 = forms.OffTroopsForm(None, outline=instance)
    form2 = forms.DeffTroopsForm(None, outline=instance)

    off_troops = Troops(instance, "off_troops")
    deff_troops = Troops(instance, "deff_troops")

    if request.method == "POST":
        if "form-1" in request.POST:
            form10 = forms.OffTroopsForm(request.POST, outline=instance)
            instance.actions.save_off_troops(instance)
            if form10.is_valid():
                instance.off_troops = request.POST["off_troops"]
                instance.off_troops_hash = instance.get_or_set_off_troops_hash(
                    force_recalculate=True
                )
                instance.save()
                request.session["message-off-troops"] = "true"
                return redirect("base:planer_detail", _id)
            else:
                off_troops.set_troops(request.POST.get("off_troops"))
                off_troops.set_errors(form10.errors)

        elif "form-2" in request.POST:
            form20 = forms.DeffTroopsForm(request.POST, outline=instance)
            instance.actions.save_deff_troops(instance)
            if form20.is_valid():
                instance.deff_troops = request.POST["deff_troops"]
                instance.save()
                instance.deff_troops_hash = instance.get_or_set_deff_troops_hash(
                    force_recalculate=True
                )
                request.session["message-deff-troops"] = "true"
                return redirect("base:planer_detail", _id)
            else:
                deff_troops.set_troops(request.POST.get("deff_troops"))
                deff_troops.set_errors(form20.errors)

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
        off_form = forms.OffTroopsForm(
            {"off_troops": instance.off_troops}, outline=instance
        )
        deff_form = forms.DeffTroopsForm(
            {"deff_troops": instance.deff_troops}, outline=instance
        )
        if not off_form.is_valid():
            off_troops.set_troops(instance.off_troops)
            off_troops.set_errors(off_form.errors)
        elif not deff_form.is_valid():
            deff_troops.set_troops(instance.deff_troops)
            deff_troops.set_errors(deff_form.errors)

    return render(request, "base/new_outline/new_outline.html", context)


@login_required
def outline_data_analysis(request: HttpRequest, _id: int) -> HttpResponse:
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )
    if not instance.off_troops or not instance.deff_troops:
        request.session["error"] = gettext(
            "<p>To use the <b><span class='md-correct'>Data analysis</span></b> tab both "
            "<b>Army collection</b> and <b>Deff collection</b> must be already filled in!</p>"
        )
        return redirect("base:planer_detail", _id)
    if instance.written == "active":
        request.session["error"] = gettext(
            "<p>You can't access <b><span class='md-correct'>Data analysis</span></b> tab, "
            "because your outline is already written! You can always click on <b>Go back</b> "
            "button in <b>Planer</b> menu tab, but you will loose part of your progress.</p>"
        )
        return redirect("base:planer_detail", _id)

    off_form = forms.OffTroopsForm(
        {"off_troops": instance.off_troops}, outline=instance
    )
    if not off_form.is_valid():
        return trigger_off_deff_troops_update_redirect(request=request, outline_id=_id)
    deff_form = forms.DeffTroopsForm(
        {"deff_troops": instance.deff_troops}, outline=instance
    )
    if not deff_form.is_valid():
        return trigger_off_deff_troops_update_redirect(request=request, outline_id=_id)

    analized_villages = OutlineTroopsAnalysis(outline=instance).run_analize()

    context = {"instance": instance, "analized_villages": analized_villages}

    return render(request, "base/new_outline/new_outline_data_analysis.html", context)
