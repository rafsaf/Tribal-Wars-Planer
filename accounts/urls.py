from django.urls import path
from django.contrib.auth import views as auth_views
from django_registration.backends.one_step.views import RegistrationView

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(success_url=''), name='registration'),
    
]

