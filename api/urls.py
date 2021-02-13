from django.urls import path
from api import views

urlpatterns = [
    path('target-time-update/<int:target_id>/<int:time_id>/', views.TargetTimeUpdate.as_view()),
    path('target-delete/<int:target_id>/', views.TargetDelete.as_view()),
]