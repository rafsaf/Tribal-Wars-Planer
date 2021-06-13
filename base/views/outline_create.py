from typing import List

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import get_language
from django.views.decorators.http import require_POST
from markdownx.utils import markdownify

from base import forms, models


@login_required
def new_outline_create(request: HttpRequest) -> HttpResponse:
    """creates new user's outline login required"""
    language_code = get_language()

    info = models.Documentation.objects.get_or_create(
        title="planer_create_info", language=language_code, defaults={"main_page": ""}
    )[0].main_page
    info = markdownify(info)
    example = models.Documentation.objects.get_or_create(
        title="planer_create_example",
        language=language_code,
        defaults={"main_page": ""},
    )[0].main_page
    example = markdownify(example)
    profile = models.Profile.objects.select_related().get(user=request.user)

    if request.method == "POST":

        form1 = forms.OutlineForm(request.POST)
        form1.fields["world"].choices = [
            (f"{world.pk}", world.human())
            for world in models.World.objects.filter(server=profile.server).order_by(
                "postfix"
            )
        ]
        if form1.is_valid():
            world = request.POST["world"]
            world_instance = get_object_or_404(models.World, pk=int(world))
            new_instance = models.Outline(
                owner=request.user,
                date=request.POST["date"],
                name=request.POST["name"],
                world=world_instance,
            )
            new_instance.save()
            new_instance.refresh_from_db()
            result = models.Result(outline=new_instance)
            result.save()
            new_instance.create_stats()

            return redirect("base:planer_create_select", new_instance.pk)
    else:
        form1 = forms.OutlineForm(None)
        form1.fields["world"].choices = [
            (f"{world.pk}", f"{world.human()}")
            for world in models.World.objects.filter(server=profile.server).order_by(
                "postfix"
            )
        ]

    context = {"form1": form1, "info": info, "example": example, "profile": profile}
    return render(request, "base/new_outline/new_outline_create.html", context)


@login_required
def new_outline_create_select(request: HttpRequest, _id: int) -> HttpResponse:
    """select user's ally and enemy tribe after creating outline, login required"""
    instance = get_object_or_404(
        models.Outline, pk=_id, owner=request.user, editable="active"
    )

    ally_tribe: List[models.Tribe] = [
        tribe
        for tribe in models.Tribe.objects.filter(
            world=instance.world, tag__in=instance.ally_tribe_tag
        )
    ]
    enemy_tribe: List[models.Tribe] = [
        tribe
        for tribe in models.Tribe.objects.filter(
            world=instance.world, tag__in=instance.enemy_tribe_tag
        )
    ]

    banned_tribe_id = [tribe.pk for tribe in ally_tribe + enemy_tribe]

    choices = [("banned", "--------")] + [  # type: ignore
        (f"{tribe.tag}", f"{tribe.tag}")
        for tribe in models.Tribe.objects.filter(world=instance.world).exclude(
            pk__in=banned_tribe_id
        )
    ]

    if request.method == "POST":
        if "tribe1" in request.POST:
            form1 = forms.MyTribeTagForm(request.POST)
            form1.fields["tribe1"].choices = choices
            form2 = forms.EnemyTribeTagForm()
            form2.fields["tribe2"].choices = choices

            if form1.is_valid():
                plemie = request.POST.get("tribe1")
                instance.ally_tribe_tag.append(plemie)
                instance.save()
                return redirect("base:planer_create_select", _id)
        elif "tribe2" in request.POST:
            form1 = forms.MyTribeTagForm()
            form1.fields["tribe1"].choices = choices
            form2 = forms.EnemyTribeTagForm(request.POST)
            form2.fields["tribe2"].choices = choices

            if form2.is_valid():
                plemie = request.POST.get("tribe2")
                instance.enemy_tribe_tag.append(plemie)
                instance.save()
                return redirect("base:planer_create_select", _id)
        else:
            form1 = forms.MyTribeTagForm()
            form1.fields["tribe1"].choices = choices
            form2 = forms.EnemyTribeTagForm()
            form2.fields["tribe2"].choices = choices

    else:
        form1 = forms.MyTribeTagForm()
        form1.fields["tribe1"].choices = choices
        form2 = forms.EnemyTribeTagForm()
        form2.fields["tribe2"].choices = choices

    context = {
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "ally": ally_tribe,
        "enemy": enemy_tribe,
    }
    return render(request, "base/new_outline/new_outline_create_select.html", context)


@require_POST
@login_required
def outline_delete_ally_tags(request: HttpRequest, _id: int) -> HttpResponse:
    """Delete ally tribe tags from outline"""
    instance = get_object_or_404(models.Outline, pk=_id, owner=request.user)
    instance.ally_tribe_tag = list()
    instance.save()
    return redirect("base:planer_create_select", _id)


@require_POST
@login_required
def outline_delete_enemy_tags(request: HttpRequest, _id: int) -> HttpResponse:
    """Delete enemy tribe tags from outline"""

    instance = get_object_or_404(models.Outline, pk=_id, owner=request.user)
    instance.enemy_tribe_tag = list()
    instance.save()
    return redirect("base:planer_create_select", _id)


@require_POST
@login_required
def outline_disable_editable(request: HttpRequest, _id: int) -> HttpResponse:
    """Outline not editable after chosing tags"""

    instance = get_object_or_404(models.Outline, pk=_id, owner=request.user)
    instance.editable = "inactive"
    instance.save()
    return redirect("base:planer")
