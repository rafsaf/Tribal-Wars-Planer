from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from base import models, forms
from markdownx.utils import markdownify

@login_required
def new_outline_create(request):
    """ creates new user's outline login required """
    language_code = get_language()

    info = models.Documentation.objects.get_or_create(title='planer_create_info', language=language_code, defaults={'main_page': ""})[0].main_page
    info = markdownify(info)
    marks = models.Documentation.objects.get_or_create(title='planer_create_marks', language=language_code, defaults={'main_page': ""})[0].main_page
    marks = markdownify(marks)
    example = models.Documentation.objects.get_or_create(title='planer_create_example', language=language_code, defaults={'main_page': ""})[0].main_page
    example = markdownify(example)

    if request.method == "POST":
        form1 = forms.OutlineForm(request.POST)
        form1.fields["world"].choices = [
            (f"{i.world}", f"{i.title}")
            for i in models.World.objects.all().order_by("-world")
        ]
        if form1.is_valid():
            new_instance = models.Outline(
                owner=request.user,
                date=request.POST["date"],
                name=request.POST["name"],
                world=request.POST["world"],
            )
            new_instance.save()
            result = models.Result(outline=new_instance)
            result.save()
            return redirect("base:planer_create_select", new_instance.id)
    else:
        form1 = forms.OutlineForm(None)
        form1.fields["world"].choices = [
            (f"{i.world}", f"{i.title}")
            for i in models.World.objects.all().order_by("-world")
        ]
    context = {"form1": form1, "info": info, "marks": marks, "example": example}
    return render(request, "base/new_outline/new_outline_create.html", context)


@login_required
def new_outline_create_select(request, _id):
    """ select user's ally and enemy tribe after creating outline, login required """
    instance = get_object_or_404(models.Outline, pk=_id, owner=request.user, editable='active')

    ally_tribe = instance.ally_tribe_tag
    enemy_tribe = instance.enemy_tribe_tag

    banned_tribe_id = [f'{tag}::{instance.world}' for tag in ally_tribe + enemy_tribe]

    choices = [("banned", "--------")] + [
        (f'{tribe.tag}', f"{tribe.tag}")
        for tribe in models.Tribe.objects.filter(world=instance.world).exclude(pk__in=banned_tribe_id)
    ]

    if request.method == 'POST':
        if "plemie1" in request.POST:
            form1 = forms.MyTribeTagForm(request.POST)
            form1.fields["plemie1"].choices = choices
            form2 = forms.EnemyTribeTagForm()
            form2.fields["plemie2"].choices = choices

            if form1.is_valid():
                plemie = request.POST.get("plemie1")
                instance.ally_tribe_tag.append(plemie)
                instance.save()
                return redirect("base:planer_create_select", _id)
        elif "plemie2" in request.POST:
            form1 = forms.MyTribeTagForm()
            form1.fields["plemie1"].choices = choices
            form2 = forms.EnemyTribeTagForm(request.POST)
            form2.fields["plemie2"].choices = choices

            if form2.is_valid():
                plemie = request.POST.get("plemie2")
                instance.enemy_tribe_tag.append(plemie)
                instance.save()
                return redirect("base:planer_create_select", _id)
    else:

        form1 = forms.MyTribeTagForm()
        form1.fields["plemie1"].choices = choices
        form2 = forms.EnemyTribeTagForm()
        form2.fields["plemie2"].choices = choices

    context = {
        "instance": instance,
        "form1": form1,
        "form2": form2,
        "ally": ally_tribe,
        "enemy": enemy_tribe,
    }
    return render(request, "base/new_outline/new_outline_create_select.html", context)

@login_required
def outline_delete_ally_tags(request, _id):
    """ Delete ally tribe tags from outline """
    if request.method == 'POST':
        instance = get_object_or_404(models.Outline, pk=_id, owner=request.user)
        instance.ally_tribe_tag = list()
        instance.save()
        return redirect("base:planer_create_select", _id)
    else:
        return Http404()

@login_required
def outline_delete_enemy_tags(request, _id):
    """ Delete enemy tribe tags from outline """
    if request.method == 'POST':
        instance = get_object_or_404(models.Outline, pk=_id, owner=request.user)
        instance.enemy_tribe_tag = list()
        instance.save()
        return redirect("base:planer_create_select", _id)
    else:
        return Http404()

@login_required
def outline_disable_editable(request, _id):
    """ Outline not editable after chosing tags"""
    if request.method == 'POST':
        instance = get_object_or_404(models.Outline, pk=_id, owner=request.user)
        instance.editable = "inactive"
        instance.save()
        return redirect("base:planer")
    else:
        return Http404()
    