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

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import signing
from django.core.mail import send_mail
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from base import forms
from base.models import Payment, Profile, Server, StripePrice

PROFILE_SALT = "profile"


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
    profile: Profile = request.user.profile  # type: ignore
    form1 = forms.ChangeProfileForm(None, instance=profile)
    if request.method == "POST":
        if "form1" in request.POST:
            form1 = forms.ChangeProfileForm(request.POST, instance=profile)
            if form1.is_valid():
                updated_profile: Profile = form1.save(commit=False)
                get_object_or_404(Server, dns=updated_profile.server)
                updated_profile.save()
                return redirect("base:settings")

        if "form2" in request.POST:
            now = timezone.now()
            exp = now + timedelta(days=settings.ACCOUNT_PERMANENT_REMOVAL_DAYS)
            token = signing.dumps(
                {
                    "pk": user.pk,
                    "iat": int(now.timestamp()),
                    "exp": exp.timestamp(),
                },
                salt=PROFILE_SALT,
                compress=True,
            )

            url = reverse("base:account_restore") + f"?token={token}"

            title = render_to_string(
                "email_delete_account_title.html",
                {"user": user},
            )
            msg_html = render_to_string(
                "email_delete_account_body.html",
                {
                    "user": user,
                    "url": url,
                    "domain": settings.MAIN_DOMAIN,
                    "ACCOUNT_PERMANENT_REMOVAL_DAYS": settings.ACCOUNT_PERMANENT_REMOVAL_DAYS,
                    "request": request,
                },
            )
            send_mail(
                title,
                "",
                from_email=None,
                recipient_list=[user.email],  # type: ignore
                html_message=msg_html,
            )

            profile.deleted_at = now
            profile.deleted_at_exp = exp
            profile.save()

            auth_logout(request)

            return redirect(reverse("base:account_removed"))

    context = {"user": user, "form1": form1}
    return render(request, "base/user/profile_settings.html", context=context)


@login_required
def premium_view(request: HttpRequest) -> HttpResponse:
    user: User = request.user  # type: ignore
    profile: Profile = user.profile  # type: ignore
    payments = Payment.objects.filter(user=user).order_by("-payment_date", "-new_date")
    prices = (
        StripePrice.objects.select_related("product")
        .filter(active=True, product__active=True, currency=profile.get_currency)
        .order_by("amount")
    )
    context = {
        "user": user,
        "payments": payments,
        "premium_account_max_targets_free": settings.PREMIUM_ACCOUNT_MAX_TARGETS_FREE,
        "prices": prices,
    }
    return render(request, "base/user/premium.html", context=context)


@login_required
@csrf_exempt
def payment_done(request: HttpRequest) -> HttpResponse:
    return render(request, "base/user/payment_done.html")


def account_removed(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "base/user/account_removed.html",
        context={
            "ACCOUNT_PERMANENT_REMOVAL_DAYS": settings.ACCOUNT_PERMANENT_REMOVAL_DAYS,
        },
    )


def account_restore(request: HttpRequest) -> HttpResponse:
    token = request.GET.get("token", "")
    try:
        obj = signing.loads(token, salt=PROFILE_SALT)
    except signing.BadSignature:
        raise Http404()

    if timezone.now().timestamp() > obj["exp"]:
        return render(request, "base/user/restore.html", context={"expired": True})

    user = get_object_or_404(User.objects.select_related("profile"), pk=obj.get("pk"))
    profile: Profile = user.profile  # type: ignore

    if int(profile.deleted_at.timestamp()) != obj["iat"]:
        return render(request, "base/user/restore.html", context={"expired": True})

    if request.method == "POST":
        if "form1" in request.POST:
            profile.deleted_at = None
            profile.deleted_at_exp = None
            profile.save()
            return redirect("base:base")

    return render(
        request,
        "base/user/restore.html",
        context={
            "recovery_user": user,
            "expired": False,
        },
    )
