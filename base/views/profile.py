from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from base import forms
from base.models import Server, Profile, Payment


@login_required
def add_world(request: HttpRequest) -> HttpResponse:
    user = request.user
    success = request.session.get("world_created")
    form1 = forms.AddNewWorldForm(None)
    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.AddNewWorldForm(request.POST)
            if form1.is_valid():
                # already created in form clean()
                request.session["world_created"] = "true"
                return redirect("base:add_world")

    context = {"user": user, "form1": form1, "message": success}
    if success is not None:
        del request.session["world_created"]
    return render(request, "base/user/add_world.html", context=context)


@login_required
def profile_settings(request: HttpRequest) -> HttpResponse:
    user = request.user
    form1 = forms.ChangeServerForm(None)
    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.ChangeServerForm(request.POST)
            if form1.is_valid():
                new_server = request.POST.get("server")
                new_server = get_object_or_404(Server, dns=new_server)
                profile: Profile = Profile.objects.get(user=user)
                profile.server = new_server
                profile.save()
                return redirect("base:settings")
    context = {"user": user, "form1": form1}
    return render(request, "base/user/profile_settings.html", context=context)


@login_required
def premium_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    payments = Payment.objects.filter(user=user).order_by("-payment_date")
    context = {"user": user, "payments": payments}
    return render(request, "base/user/premium.html", context=context)
