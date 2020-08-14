from django.urls import path, include
from django.contrib.auth import views as auth_views
from django_registration.backends.one_step.views import RegistrationView
from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    path('', include('django_registration.backends.one_step.urls')),
    path('', include('django.contrib.auth.urls')),
    
]

