from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language, gettext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from markdownx.utils import markdownify

from base import models, forms


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
            outline.world_human = outline.world.human(prefix=True)
            outline.ally_tribe_tag = ", ".join(outline.ally_tribe_tag)
            outline.enemy_tribe_tag = ", ".join(outline.enemy_tribe_tag)
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
            outline.world_human = outline.world.human(prefix=True)
            outline.ally_tribe_tag = ", ".join(outline.ally_tribe_tag)
            outline.enemy_tribe_tag = ", ".join(outline.enemy_tribe_tag)
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
    language_code = get_language()

    info = models.Documentation.objects.get_or_create(
        title="planer_script_info", language=language_code, defaults={"main_page": ""}
    )[0].main_page
    info = markdownify(info)
    example = models.Documentation.objects.get_or_create(
        title="planer_script_example",
        language=language_code,
        defaults={"main_page": ""},
    )[0].main_page
    example = markdownify(example)

    form1 = forms.OffTroopsForm(None, outline=instance)
    form2 = forms.DeffTroopsForm(None, outline=instance)

    form1.fields["off_troops"].initial = instance.off_troops
    form2.fields["deff_troops"].initial = instance.deff_troops

    if request.method == "POST":
        if "form-1" in request.POST:
            form1 = forms.OffTroopsForm(request.POST, outline=instance)
            if form1.is_valid():
                instance.off_troops = request.POST.get("off_troops")
                instance.save()
                request.session["message-off-troops"] = "true"
                return redirect("base:planer_detail", _id)

        elif "form-2" in request.POST:
            form2 = forms.DeffTroopsForm(request.POST, outline=instance)
            if form2.is_valid():
                instance.deff_troops = request.POST.get("deff_troops")
                instance.save()
                request.session["message-deff-troops"] = "true"
                return redirect("base:planer_detail", _id)

    if instance.world.postfix == "Test":
        instance.world.update = gettext("Never") + "."
    else:
        _timedelta = timezone.now() - instance.world.last_update
        instance.world.update = str(_timedelta.seconds // 60) + gettext(
            " minute(s) ago."
        )

    context = {
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "example": example,
        "info": info,
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
