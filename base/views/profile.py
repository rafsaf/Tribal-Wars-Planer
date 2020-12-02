from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tribal_wars.database_update import WorldQuery
from base import models, forms

@login_required
def add_world(request):
    user = request.user

    form1 = forms.AddNewWorldForm(None)
    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.AddNewWorldForm(request.POST)
            if form1.is_valid():
                # already created in form clean()
                return redirect("base:add_world")

    context = {"user": user, "form1": form1}
    return render(request, "base/user/add_world.html", context=context)

@login_required
def profile_settings(request):
    user = request.user


    context = {"user": user}
    return render(request, "base/user/profile_settings.html", context=context)