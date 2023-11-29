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
from django.views.decorators.http import require_POST

from base import forms, models
from base.models.profile import Profile


@login_required
def new_outline_create(request: HttpRequest) -> HttpResponse:
    """creates new user's outline login required"""
    profile: Profile = models.Profile.objects.select_related().get(user=request.user)
    form1 = forms.OutlineForm(None)
    form2 = forms.ChangeServerForm(None)

    form1.fields["world"].choices = [
        (f"{world.pk}", f"{world.human()}")
        for world in models.World.objects.filter(server=profile.server).order_by(
            "postfix"
        )
    ]
    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.OutlineForm(request.POST)
            form1.fields["world"].choices = [
                (f"{world.pk}", world.human())
                for world in models.World.objects.filter(
                    server=profile.server
                ).order_by("postfix")
            ]
            if form1.is_valid():
                world = request.POST["world"]
                world_instance = get_object_or_404(models.World, pk=int(world))
                new_instance = models.Outline(
                    owner=request.user,
                    date=request.POST["date"],
                    name=request.POST["name"],
                    world=world_instance,
                    morale_on=profile.default_morale_on,
                    initial_outline_target_dist=world_instance.max_noble_distance,
                    input_data_type=profile.input_data_type,
                    sending_option=profile.sending_option,
                    send_message_with_url=profile.send_message_with_url,
                    title_message=profile.send_message_title_message,
                    text_message=profile.send_message_text_message,
                )
                new_instance.save()
                new_instance.refresh_from_db()
                result = models.Result(outline=new_instance)
                result.save()
                new_instance.create_stats()

                return redirect("base:planer_create_select", new_instance.pk)
        if "form2" in request.POST:
            form2 = forms.ChangeServerForm(request.POST)
            if form2.is_valid():
                new_server = request.POST.get("server")
                new_server = get_object_or_404(models.Server, dns=new_server)
                profile: models.Profile = models.Profile.objects.get(user=request.user)
                profile.server = new_server
                profile.server_bind = True
                profile.save()
                return redirect("base:planer_create")

    context = {"form1": form1, "profile": profile, "form2": form2}
    return render(request, "base/new_outline/new_outline_create.html", context)


@login_required
def new_outline_create_select(  # noqa: PLR0912
    request: HttpRequest, _id: int
) -> HttpResponse:
    """select user's ally and enemy tribe after creating outline, login required"""
    instance = get_object_or_404(
        models.Outline, pk=_id, owner=request.user, editable="active"
    )

    ally_tribe: list[models.Tribe] = [
        tribe
        for tribe in models.Tribe.objects.filter(
            world=instance.world, tag__in=instance.ally_tribe_tag
        )
    ]
    enemy_tribe: list[models.Tribe] = [
        tribe
        for tribe in models.Tribe.objects.filter(
            world=instance.world, tag__in=instance.enemy_tribe_tag
        )
    ]

    banned_tribe_id = [tribe.pk for tribe in ally_tribe + enemy_tribe]

    choices = [("banned", "--------")] + [
        (f"{tribe.tag}", f"{tribe.tag}")
        for tribe in models.Tribe.objects.filter(world=instance.world).exclude(
            pk__in=banned_tribe_id
        )
    ]

    sugested_ally_tribes = []
    sugested_enemy_tribes = []
    for old_outline in (
        models.Outline.objects.filter(world=instance.world, owner=request.user)
        .exclude(id=_id)
        .order_by("-created")[:5]
    ):
        for old_ally_tribe_tag in old_outline.ally_tribe_tag:
            if (old_ally_tribe_tag, old_ally_tribe_tag) in choices:
                if (
                    len(sugested_ally_tribes) < 6
                    and old_ally_tribe_tag not in sugested_ally_tribes
                ):
                    sugested_ally_tribes.append(old_ally_tribe_tag)
        for old_enemy_tribe_tag in old_outline.enemy_tribe_tag:
            if (old_enemy_tribe_tag, old_enemy_tribe_tag) in choices:
                if (
                    len(sugested_enemy_tribes) < 6
                    and old_enemy_tribe_tag not in sugested_enemy_tribes
                ):
                    sugested_enemy_tribes.append(old_enemy_tribe_tag)

    if request.method == "POST":
        if "tribe1" in request.POST:
            form1 = forms.MyTribeTagForm(request.POST)
            form1.fields["tribe1"].choices = choices
            form2 = forms.EnemyTribeTagForm()
            form2.fields["tribe2"].choices = choices

            if form1.is_valid():
                tribe = request.POST["tribe1"]
                instance.ally_tribe_tag.append(tribe)
                instance.save()
                return redirect("base:planer_create_select", _id)
        elif "tribe2" in request.POST:
            form1 = forms.MyTribeTagForm()
            form1.fields["tribe1"].choices = choices
            form2 = forms.EnemyTribeTagForm(request.POST)
            form2.fields["tribe2"].choices = choices

            if form2.is_valid():
                tribe = request.POST["tribe2"]
                instance.enemy_tribe_tag.append(tribe)
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
        "sugested_ally_tribes": sugested_ally_tribes,
        "sugested_enemy_tribes": sugested_enemy_tribes,
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
