from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from tribal_wars.get_deff import get_deff
from base import models, forms
from django.utils.translation import gettext


@login_required
def outline_detail_2_deff(request, _id):
    """ details user outline, get deff page """
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    result = get_object_or_404(models.Result, pk=instance)

    # only correct deff_troops allowed
    if instance.deff_troops == "":
        request.session["error"] = gettext("Deff collection empty!")
        return redirect("base:planer_detail", _id)
    if instance.off_troops == "":
        request.session["error"] = gettext("Off collection empty!")
        return redirect("base:planer_detail", _id)

    form = forms.GetDeffForm(request.POST or None, world=instance.world)
    if "form" in request.POST:
        if form.is_valid():
            try:
                result.results_get_deff = get_deff(
                    outline=instance,
                    radius=int(request.POST.get("radius")),
                    ally_name_list=request.POST.get("ally_players"),
                    enemy_name_list=request.POST.get("enemy_players"),
                    excluded_villages=request.POST.get("excluded"),
                )
            except KeyError:
                request.session["error"] = gettext(
                    "It looks like your Deff or Off collection is no longer actual! To use the planner: copy the data from the preview and correct errors or paste the current military data \n"
                )
                return redirect("base:planer_detail", _id)

            result.save()

            return redirect("base:planer_detail_results", _id)

    context = {"instance": instance, "form": form}

    return render(
        request, "base/new_outline/new_outline_get_deff.html", context
    )


@login_required
def outline_detail_2_off(request, _id):
    """ details user outline, get off page """
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    result = get_object_or_404(models.Result, pk=instance)

    # only correct deff and off troops allowed
    if instance.deff_troops == "":
        request.session["error"] = gettext("Deff collection empty!")
        return redirect("base:planer_detail", _id)
    if instance.off_troops == "":
        request.session["error"] = gettext("Off collection empty!")
        return redirect("base:planer_detail", _id)

    form = forms.GetDeffForm(request.POST or None, world=instance.world)
    if "form" in request.POST:
        if form.is_valid():
            try:
                result.results_get_off = get_deff(
                    outline=instance,
                    radius=int(request.POST.get("radius")),
                    ally_name_list=request.POST.get("ally_players"),
                    enemy_name_list=request.POST.get("enemy_players"),
                    excluded_villages=request.POST.get("excluded"),
                    deff=False,
                )
            except KeyError:
                request.session["error"] = gettext(
                    "It looks like your Deff or Off collection is no longer actual! To use the planner: copy the data from the preview and correct errors or paste the current military data \n"
                )
                return redirect("base:planer_detail", _id)

            result.save()

            return redirect("base:planer_detail_results", _id)

    context = {"instance": instance, "form": form}

    return render(
        request, "base/new_outline/new_outline_get_off.html", context
    )


@login_required
def outline_detail_results(request, _id):
    """ view for results """

    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)

    overviews = models.Overview.objects.filter(outline=instance).order_by(
        "token"
    )

    world = models.World.objects.get(world=instance.world)

    if world.classic:
        name_prefix = 'cl'
    else:
        name_prefix = 'pl'

    context = {"instance": instance, "overviews": overviews, "name_prefix": name_prefix}

    return render(
        request, "base/new_outline/new_outline_results.html", context
    )
