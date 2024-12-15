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

from base.views.home import (
    base_documentation,
    base_view,
    overview_view,
    payment_sum_up_view,
)
from base.views.outline import (
    inactive_outline,
    outline_delete,
    outline_detail,
    outline_list,
)
from base.views.outline_create import (
    new_outline_create,
    new_outline_create_select,
    outline_delete_ally_tags,
    outline_delete_enemy_tags,
    outline_disable_editable,
)
from base.views.outline_initial_changes import (
    initial_add_first,
    initial_add_first_fake,
    initial_add_first_fake_noble,
    initial_add_first_off,
    initial_add_first_ruin,
    initial_add_last,
    initial_add_last_fake,
    initial_add_last_fake_noble,
    initial_add_last_off,
    initial_add_last_ruin,
    initial_divide,
    initial_hide_weight,
    initial_move_down,
    initial_move_up,
    initial_weight_delete,
)
from base.views.outline_initial_views import (
    complete_outline,
    initial_delete_time,
    initial_form,
    initial_planer,
    initial_set_all_time,
    initial_set_all_time_page,
    initial_target,
)
from base.views.profile import add_world, payment_done, premium_view, profile_settings
from base.views.results_get_deff import outline_detail_get_deff, outline_detail_results

app_name = "base"

urlpatterns = [
    path("", base_view, name="base"),
    path("profile/user-settings", profile_settings, name="settings"),
    path("profile/add-world", add_world, name="add_world"),
    path("profile/premium", premium_view, name="premium"),
    path("profile/payment-done", payment_done, name="payment_done"),
    path(
        "profile/auth/payments-summary",
        payment_sum_up_view,
        name="payment_summary",
    ),
    path("overview/<str:token>", overview_view, name="overview"),
    path("planer/", outline_list, name="planer"),
    path("planer/create/", new_outline_create, name="planer_create"),
    path("planer/<int:_id>/status", inactive_outline, name="planer_status"),
    path("planer/<int:_id>", outline_detail, name="planer_detail"),
    path("planer/<int:_id>/delete", outline_delete, name="planer_delete"),
    path("documentation/", base_documentation, name="documentation"),
    path(
        "planer/<int:_id>/delete/ally-tags",
        outline_delete_ally_tags,
        name="planer_delete_ally_tags",
    ),
    path(
        "planer/<int:_id>/delete/enemy-tags",
        outline_delete_enemy_tags,
        name="planer_delete_enemy_tags",
    ),
    path(
        "planer/<int:_id>/disable_editable",
        outline_disable_editable,
        name="planer_disable_editable",
    ),
    path(
        "planer/<int:_id>/results",
        outline_detail_results,
        name="planer_detail_results",
    ),
    path(
        "planer/<int:_id>/planer-form",
        initial_form,
        name="planer_initial_form",
    ),
    path(
        "planer/<int:_id>/planer-menu",
        initial_planer,
        name="planer_initial",
    ),
    path(
        "planer/<int:id1>/complete",
        complete_outline,
        name="planer_complete",
    ),
    path(
        "planer/planer-menu/delete-time/<int:pk>",
        initial_delete_time,
        name="planer_delete_time",
    ),
    path(
        "planer/planer-menu/set-all-time/<int:pk>",
        initial_set_all_time,
        name="planer_set_all_time",
    ),
    path(
        "planer/planer-menu/set-all-time-page/<int:pk>",
        initial_set_all_time_page,
        name="planer_set_all_time_page",
    ),
    path(
        "planer/<int:id1>/planer-target/<int:id2>",
        initial_target,
        name="planer_initial_detail",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_first",
        initial_add_first,
        name="planer_add_first",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_first_off",
        initial_add_first_off,
        name="planer_add_first_off",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_first_ruin",
        initial_add_first_ruin,
        name="planer_add_first_ruin",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_first_fake",
        initial_add_first_fake,
        name="planer_add_first_fake",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_first_fake_noble",
        initial_add_first_fake_noble,
        name="planer_add_first_fake_noble",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_last_fake",
        initial_add_last_fake,
        name="planer_add_last_fake",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_last_fake_noble",
        initial_add_last_fake_noble,
        name="planer_add_last_fake_noble",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_last_ruin",
        initial_add_last_ruin,
        name="planer_add_last_ruin",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_last",
        initial_add_last,
        name="planer_add_last",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/add_last_off",
        initial_add_last_off,
        name="planer_add_last_off",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id3>/hide",
        initial_hide_weight,
        name="planer_hide_weight",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id4>/up",
        initial_move_up,
        name="planer_move_up",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id4>/<int:n>",
        initial_divide,
        name="planer_divide",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id4>/down",
        initial_move_down,
        name="planer_move_down",
    ),
    path(
        "planer/<int:id1>/<int:id2>/<int:id4>/delete",
        initial_weight_delete,
        name="planer_initial_delete",
    ),
    path(
        "planer/<int:_id>/get-deff",
        outline_detail_get_deff,
        name="planer_detail_get_deff",
    ),
    path(
        "planer/<int:_id>/create/select-tribe",
        new_outline_create_select,
        name="planer_create_select",
    ),
]
