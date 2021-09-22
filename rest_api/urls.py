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
