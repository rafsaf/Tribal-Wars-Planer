from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from trbial_wars.get_deff import get_deff
from base import models, forms


@login_required
def outline_detail_2_deff(request, _id):
    """ details user outline, get deff page """
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    result = get_object_or_404(models.Result, pk=instance)

    # only correct deff_troops allowed
    if instance.deff_troops == "":
        request.session["error"] = "Zbiórka Obrona pusta !"
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
                request.session[
                    "error"
                ] = "Wygląda na to, że Twoja Zbiórka Obrona nie jest już aktualna! Aby skorzystać z Zbiórki Deffa: skopiuj dane z podglądu i popraw błędy lub wklej aktualne dane o obronie. \n"
                return redirect("base:planer_detail", _id)



            result.save()

            return redirect("base:planer_detail_get_deff", _id)

    context = {"instance": instance, "form": form}

    return render(request, "base/new_outline/new_outline_get_deff.html", context)


def outline_detail_results(request, _id):
    """ view for results """

    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)

    context = {"instance": instance}

    return render(request, "base/new_outline/new_outline_results.html", context)
