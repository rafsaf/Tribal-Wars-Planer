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
    path("stripe-key/", views.stripe_config, name="stripe_key"),
    path("stripe-session/", views.stripe_checkout_session, name="stripe_session"),
    path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("target-time-update/", views.target_time_update, name="target_time_update"),
    path("target-delete/", views.delete_target, name="target_delete"),
    path(
        "overview-hide-state-update/",
        views.overview_state_update,
        name="hide_state_update",
    ),
    path(
        "change-buildings-array/",
        views.change_buildings_array,
        name="change_buildings_array",
    ),
    path(
        "change-weight-building/",
        views.change_weight_model_buildings,
        name="change_weight_building",
    ),
    path("reset-user-messages/", views.reset_user_messages, name="reset_user_messages"),
    path("metrics/", views.metrics_export, name="metrics_export"),
    path("healthcheck/", views.healthcheck, name="healthcheck"),
]
