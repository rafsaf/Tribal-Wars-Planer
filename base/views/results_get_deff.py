from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from tribal_wars.get_deff import get_deff
from tribal_wars import basic
from base import models, forms
from django.utils.translation import gettext
from django.utils.translation import get_language
from markdownx.utils import markdownify


@login_required
def outline_detail_get_deff(request, _id):
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

    info = models.Documentation.objects.get_or_create(
        title="planer_deff_info",
        language=language_code,
        defaults={"main_page": ""},
    )[0].main_page
    info = markdownify(info)
    marks = models.Documentation.objects.get_or_create(
        title="planer_deff_marks",
        language=language_code,
        defaults={"main_page": ""},
    )[0].main_page
    marks = markdownify(marks)
    example = models.Documentation.objects.get_or_create(
        title="planer_deff_example",
        language=language_code,
        defaults={"main_page": ""},
    )[0].main_page
    example = markdownify(example)

    form = forms.GetDeffForm(request.POST or None, world=instance.world)
    if "form" in request.POST:
        if form.is_valid():
            try:
                result.results_get_deff = get_deff(
                    outline=instance,
                    radius=int(request.POST.get("radius")),
                    excluded_villages=request.POST.get("excluded"),
                )
            except basic.DeffException:
                request.session["error"] = gettext(
                    "It looks like your Deff or Off collection is no longer actual! To use the planner: copy the data from the preview and correct errors or paste the current military data \n"
                )
                return redirect("base:planer_detail", _id)

            result.save()

            return redirect("base:planer_detail_results", _id)

    context = {
        "instance": instance,
        "form": form,
        "info": info,
        "example": example,
        "marks": marks,
    }

    return render(
        request, "base/new_outline/new_outline_get_deff.html", context
    )


@login_required
def outline_detail_results(request, _id):
    """ view for results """
    instance = get_object_or_404(models.Outline.objects.select_related(), id=_id, owner=request.user)
    overviews = models.Overview.objects.filter(outline=instance, removed=False).order_by(
        "player"
    )
    removed_overviews = models.Overview.objects.filter(outline=instance, removed=True).order_by("-created", "player")
    world = instance.world
    name_prefix = world.link_to_game()

    form1 = forms.SettingMessageForm(request.POST or None)
    form1.fields["default_show_hidden"].initial = instance.default_show_hidden
    form1.fields["title_message"].initial = instance.title_message
    form1.fields["text_message"].initial = instance.text_message.replace(
        "%0A", "\r\n"
    ).replace("+", " ")

    if request.method == "POST":
        if "form1" in request.POST:
            if form1.is_valid():
                default_show_hidden = request.POST.get("default_show_hidden")
                
                if default_show_hidden == "on":
                    default_show_hidden = True
                else:
                    default_show_hidden = False

                title_message = request.POST.get("title_message")
                text_message = request.POST.get("text_message").strip()
                instance.default_show_hidden = default_show_hidden
                instance.title_message = title_message
                instance.text_message = text_message.replace(
                    "\r\n", "%0A"
                ).replace(" ", "+")
                instance.save()

                overviews_update_lst = []
                for overview in overviews:
                    overview.show_hidden = default_show_hidden
                    overviews_update_lst.append(overview)
                models.Overview.objects.bulk_update(
                    overviews_update_lst, fields=["show_hidden"]
                )
                return redirect("base:planer_detail_results", _id)

    context = {
        "instance": instance,
        "overviews": overviews,
        "removed_overviews": removed_overviews,
        "name_prefix": name_prefix,
        "form1": form1,
    }

    return render(
        request, "base/new_outline/new_outline_results.html", context
    )
