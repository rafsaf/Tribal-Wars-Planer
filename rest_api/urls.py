from django.urls import path

from rest_api import views

app_name = "rest_api"

urlpatterns = [
    path("stripe-key/", views.StripeConfig.as_view(), name="stripe_key"),
    path(
        "stripe-session/<int:amount>",
        views.StripeCheckoutSession.as_view(),
        name="stripe_session",
    ),
    path("stripe-webhook/", views.StripeWebhook.as_view(), name="stripe_webhook"),
    path(
        "target-time-update/<int:target_id>/<int:time_id>/",
        views.TargetTimeUpdate.as_view(),
        name="target_time_update",
    ),
    path(
        "target-delete/<int:target_id>/",
        views.TargetDelete.as_view(),
        name="target_delete",
    ),
    path(
        "overview-hide-state-update/<int:outline_id>/<str:token>/",
        views.OverwiewStateHideUpdate.as_view(),
        name="hide_state_update",
    ),
    path(
        "change-buildings-array/<int:outline_id>/",
        views.ChangeBuildingsArray.as_view(),
        name="change_buildings_array",
    ),
    path(
        "change-weight-building/<int:outline_id>/<int:weight_id>/",
        views.ChangeWeightModelBuilding.as_view(),
        name="change_weight_building",
    ),
    path(
        "reset-user-messages/",
        views.ResetUserMessages.as_view(),
        name="reset_user_messages",
    ),
]
