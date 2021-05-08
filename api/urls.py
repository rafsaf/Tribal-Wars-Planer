from django.urls import path
from api import views

urlpatterns = [
    path(
        "target-time-update/<int:target_id>/<int:time_id>/",
        views.TargetTimeUpdate.as_view(),
    ),
    path("target-delete/<int:target_id>/", views.TargetDelete.as_view()),
    path(
        "overview-hide-state-update/<int:outline_id>/<str:token>/",
        views.OverwiewStateHideUpdate.as_view(),
    ),
    path(
        "change-buildings-array/<int:outline_id>/", views.ChangeBuildingsArray.as_view()
    ),
    path("reset-user-messages/", views.ResetUserMessages.as_view()),
]
