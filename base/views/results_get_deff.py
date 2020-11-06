from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from tribal_wars.get_deff import get_deff
from base import models, forms
from django.utils.translation import gettext
from django.utils.translation import get_language
from markdownx.utils import markdownify

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

    language_code = get_language()

    info = models.Documentation.objects.get_or_create(title='planer_deff_info', language=language_code, defaults={'main_page': ""})[0].main_page
    info = markdownify(info)
    marks = models.Documentation.objects.get_or_create(title='planer_deff_marks', language=language_code, defaults={'main_page': ""})[0].main_page
    marks = markdownify(marks)
    example = models.Documentation.objects.get_or_create(title='planer_deff_example', language=language_code, defaults={'main_page': ""})[0].main_page
    example = markdownify(example)


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

    context = {"instance": instance, "form": form, "info": info,
        "example": example, "marks": marks}

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

    language_code = get_language()

    info = models.Documentation.objects.get_or_create(title='planer_off_info', language=language_code, defaults={'main_page': ""})[0].main_page
    info = markdownify(info)
    marks = models.Documentation.objects.get_or_create(title='planer_off_marks', language=language_code, defaults={'main_page': ""})[0].main_page
    marks = markdownify(marks)
    example = models.Documentation.objects.get_or_create(title='planer_off_example', language=language_code, defaults={'main_page': ""})[0].main_page
    example = markdownify(example)

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

    context = {"instance": instance, "form": form, "info": info, "marks": marks, "example": example}

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
        name_prefix = 'c'
    else:
        name_prefix = ''

    context = {"instance": instance, "overviews": overviews, "name_prefix": name_prefix}

    return render(
        request, "base/new_outline/new_outline_results.html", context
    )
