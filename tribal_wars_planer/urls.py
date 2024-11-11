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

"""tribal_wars_planer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path
from django.views.generic.base import TemplateView
from django_registration.backends.activation.views import (
    ActivationView,
    RegistrationView,
)
from django_registration.forms import RegistrationFormCaseInsensitive
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path("api/", include("rest_api.urls")),
    path("api/public/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/public/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/public/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += i18n_patterns(  # type: ignore
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("", include(tf_urls)),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "activate/complete/",
        TemplateView.as_view(
            template_name="django_registration/activation_complete.html"
        ),
        name="django_registration_activation_complete",
    ),
    path(
        "activate/<str:activation_key>/",
        ActivationView.as_view(),
        name="django_registration_activate",
    ),
    path(
        "register/",
        RegistrationView.as_view(form_class=RegistrationFormCaseInsensitive),
        name="django_registration_register",
    ),
    path(
        "register/complete/",
        TemplateView.as_view(
            template_name="django_registration/registration_complete.html"
        ),
        name="django_registration_complete",
    ),
    path(
        "register/disallowed/",
        TemplateView.as_view(
            template_name="django_registration/registration_disallowed.html"
        ),
        name="django_registration_disallowed",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
if settings.DEBUG_TOOLBAR:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
