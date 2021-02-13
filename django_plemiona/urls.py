"""django_plemiona URL Configuration

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
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django_registration.backends.one_step.views import RegistrationView
from django_plemiona import forms

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('api.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('register/', RegistrationView.as_view(form_class=forms.RecaptchaRegistrationForm), name='django_registration_register'),
    path('', include('django_registration.backends.one_step.urls')),
    path('', include('django.contrib.auth.urls')),
    
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
