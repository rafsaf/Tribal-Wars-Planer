from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from base import models, forms


class OutlineList(LoginRequiredMixin, ListView):
    """ login required view /planer """

    template_name = "base/base_planer.html"

    def get_queryset(self):
        models.Outline.objects.filter(editable='active').delete()
        query = models.Outline.objects.filter(owner=self.request.user).filter(
            status="active"
        )
        used_worlds = {}
        for outline in query:
            if outline.world in used_worlds:
                outline.world = used_worlds[outline.world]
            else:
                world_instance = models.World.objects.get(world=outline.world)
                used_worlds[outline.world] = world_instance.title
                outline.world = used_worlds[outline.world]

            outline.ally_tribe_tag = ", ".join(outline.ally_tribe_tag)
            outline.enemy_tribe_tag = ", ".join(outline.enemy_tribe_tag)
        return query

class OutlineListShowAll(LoginRequiredMixin, ListView):
    """ login required view which shows hidden instances /planer/show_all """

    template_name = "base/base_planer.html"

    def get_queryset(self):
        models.Outline.objects.filter(editable='active').delete()
        query = models.Outline.objects.filter(owner=self.request.user)
        used_worlds = {}
        for outline in query:
            if outline.world in used_worlds:
                outline.world = used_worlds[outline.world]
            else:
                world_instance = models.World.objects.get(world=outline.world)
                used_worlds[outline.world] = world_instance.title
                outline.world = used_worlds[outline.world]
            outline.ally_tribe_tag = ", ".join(outline.ally_tribe_tag)
            outline.enemy_tribe_tag = ", ".join(outline.enemy_tribe_tag)
        return query
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_all"] = True
        return context


@login_required
@require_POST
def inactive_outline(request, _id):
    """ class based view makeing outline with id=id inavtive/active, post and login required """

    outline = get_object_or_404(models.Outline, id=_id, owner=request.user)
    if outline.status == "active":
        outline.status = "inactive"
        outline.save()
        return redirect("base:planer")
    else:
        outline.status = "active"
        outline.save()
        return redirect("base:planer_all")


class OutlineDelete(LoginRequiredMixin, DeleteView):
    """ class based view to delete outline login required"""

    model = models.Outline
    success_url = reverse_lazy("base:planer")


@login_required
def outline_detail_1(request, _id):
    """details user's outline , login required"""
    models.Outline.objects.filter(editable='active').delete()
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)

    if request.method == "POST":
        if "form-1" in request.POST:
            post = request.POST.copy()
            post['off_troops'] = post['off_troops'].strip()
            form1 = forms.OffTroopsForm(post, outline=instance)
            form2 = forms.DeffTroopsForm(None, outline=instance)
            if form1.is_valid():
                instance.off_troops = post['off_troops']
                instance.save()
                return redirect("base:planer_detail", _id)

        if "form-2" in request.POST:
            post = request.POST.copy()
            post['deff_troops'] = post['deff_troops'].strip()
            form1 = forms.OffTroopsForm(None, outline=instance)
            form2 = forms.DeffTroopsForm(post, outline=instance)
            if form2.is_valid():
                instance.deff_troops = post['deff_troops']
                instance.save()
                return redirect("base:planer_detail", _id)
    else:
        form1 = forms.OffTroopsForm(None, outline=instance)
        form2 = forms.DeffTroopsForm(None, outline=instance)

    context = {"instance": instance, "form1": form1, "form2": form2}

    error = request.session.get("error")
    if error is not None:
        context["error"] = error
        del request.session["error"]
    return render(request, "base/new_outline/new_outline.html", context)
