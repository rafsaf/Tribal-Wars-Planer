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

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext

from base import forms, models
from utils import basic
from utils.basic import encode_component
from utils.get_deff import get_deff


@login_required
def outline_detail_get_deff(request: HttpRequest, _id: int) -> HttpResponse:
    """details user outline, get deff page"""
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    result = get_object_or_404(models.Result, pk=instance)

    # only correct deff_troops allowed
    if instance.deff_troops == "":
        request.session["error"] = gettext("<h5>Deff collection is empty!</h5>")
        return redirect("base:planer_detail", _id)
    if instance.off_troops == "":
        request.session["error"] = gettext("<h5>Army collection is empty!</h5>")
        return redirect("base:planer_detail", _id)

    form = forms.GetDeffForm(request.POST or None, world=instance.world)
    if "form" in request.POST:
        if form.is_valid():
            try:
                result.results_get_deff = get_deff(
                    outline=instance,
                    radius=int(request.POST.get("radius") or 0),
                    excluded_villages=request.POST.get("excluded", ""),
                )
            except basic.DeffException:
                request.session["error"] = gettext(
                    "<h5>It looks like your Army or Deff collections are no longer actual!</h5> <p>To use the Deff collection:</p> <p>1. Paste the current data in the <b>Army and Deff collections</b> and <b>Submit</b> both.</p> <p>2. Return to the <b>Deff collection</b> tab.</p> <p>3. Try again."
                )
                return redirect("base:planer_detail", _id)

            result.save()

            return redirect(
                reverse("base:planer_detail_results", args=[_id]) + "?tab=deff"
            )

    context = {
        "instance": instance,
        "form": form,
    }

    return render(request, "base/new_outline/new_outline_get_deff.html", context)


@login_required
def outline_detail_results(request: HttpRequest, _id: int) -> HttpResponse:
    """view for results"""
    instance: models.Outline = get_object_or_404(
        models.Outline.objects.select_related(), id=_id, owner=request.user
    )
    overviews = models.Overview.objects.filter(
        outline=instance, removed=False
    ).order_by("player")
    removed_overviews = models.Overview.objects.filter(
        outline=instance, removed=True
    ).order_by("-created", "player")
    world: models.World = instance.world
    name_prefix = world.link_to_game()

    form1 = forms.SettingMessageForm(request.POST or None)
    form1.fields["default_show_hidden"].initial = instance.default_show_hidden
    form1.fields["title_message"].initial = instance.title_message
    form1.fields["text_message"].initial = instance.text_message
    form1.fields["sending_option"].initial = instance.sending_option

    if request.method == "POST":
        if "form1" in request.POST:
            if form1.is_valid():
                default_show_hidden = request.POST.get("default_show_hidden")

                if default_show_hidden == "on":
                    default_show_hidden = True
                else:
                    default_show_hidden = False

                title_message = request.POST.get("title_message")
                text_message = request.POST.get("text_message")
                sending_option = request.POST.get("sending_option")
                instance.sending_option = sending_option
                instance.default_show_hidden = default_show_hidden
                instance.title_message = title_message
                instance.text_message = text_message
                instance.save()

                overviews.update(show_hidden=default_show_hidden)

                return redirect("base:planer_detail_results", _id)

    subject = encode_component(instance.title_message)
    context = {
        "instance": instance,
        "overviews": overviews,
        "removed_overviews": removed_overviews,
        "name_prefix": name_prefix,
        "form1": form1,
        "subject": subject,
    }
    tab = request.GET.get("tab")
    if tab == "deff":
        context["go_deff_tab"] = True

    error_messages = request.session.get("error_messages")
    if error_messages is not None:
        errors = error_messages.split(",")
        context["error"] = errors
        del request.session["error_messages"]

    item: models.Overview
    for item in [i for i in overviews] + [i for i in removed_overviews]:
        item.extend_with_encodeURIComponent(instance, request)

    return render(request, "base/new_outline/new_outline_results.html", context)
