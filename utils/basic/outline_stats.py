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

from django.db.models import F

from base.models import Outline, Stats


class Action:
    def save_off_troops(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(off_troops=F("off_troops") + 1)

    def save_deff_troops(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(deff_troops=F("deff_troops") + 1)

    def save_real_targets(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(real_targets=F("real_targets") + 1)

    def save_fake_targets(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(fake_targets=F("fake_targets") + 1)

    def save_ruin_targets(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(ruin_targets=F("ruin_targets") + 1)

    def click_troops_refresh(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(
            troops_refreshed=F("troops_refreshed") + 1
        )

    def click_outline_write(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(
            outline_written=F("outline_written") + 1
        )

    def form_available_troops(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(
            available_troops=F("available_troops") + 1
        )

    def form_date_change(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(date_change=F("date_change") + 1)

    def form_settings_change(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(
            settings_change=F("settings_change") + 1
        )

    def form_night_change(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(night_change=F("night_change") + 1)

    def form_ruin_change(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(ruin_change=F("ruin_change") + 1)

    def form_building_order_change(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(
            building_order_change=F("building_order_change") + 1
        )

    def save_time_created(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(time_created=F("time_created") + 1)

    def click_go_back(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(
            go_back_clicked=F("go_back_clicked") + 1
        )

    def click_outline_finish(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(
            finish_outline_clicked=F("finish_outline_clicked") + 1
        )

    def visit_overview_visited(self, outline: Outline) -> None:
        Stats.objects.filter(outline=outline).update(
            overview_visited=F("overview_visited") + 1
        )


action: Action = Action()
