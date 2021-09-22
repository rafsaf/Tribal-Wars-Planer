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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django_registration.backends.one_step.views import RegistrationView

from tribal_wars_planer import forms

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("api/", include("rest_api.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "register/",
        RegistrationView.as_view(form_class=forms.RecaptchaRegistrationForm),
        name="django_registration_register",
    ),
    path("", include("django_registration.backends.one_step.urls")),
    path("", include("django.contrib.auth.urls")),
)
