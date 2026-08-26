# Copyright 2026 Rafał Safin (rafsaf). All Rights Reserved.
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

from datetime import date

import pytest
from django.urls import reverse

from base.models import Outline
from base.tests.test_utils.mini_setup import MiniSetup


class InitialPlanerOutlineDate(MiniSetup):
    def test_planer_initial___200_renders_edit_outline_date_modal(self) -> None:
        outline = self.get_outline(written="active")
        path = reverse("base:planer_initial", args=[outline.pk])

        self.login_me()
        response = self.client.get(path)

        assert response.status_code == 200
        content = response.content.decode()
        assert 'data-bs-target="#OutlineDateModal"' in content
        assert "bi-pencil-square" in content
        assert "Finish the Outline" in content
        assert "results are regenerated with the updated date" in content

    def test_planer_initial___302_updates_outline_date_from_menu_modal(self) -> None:
        outline = self.get_outline(written="active")
        path = reverse("base:planer_initial", args=[outline.pk])
        called_with: list[int] = []

        def fake_form_date_change(saved_outline: Outline) -> None:
            called_with.append(saved_outline.pk)

        self.login_me()
        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setattr(
                outline.actions,
                "form_date_change",
                fake_form_date_change,
            )
            response = self.client.post(
                path + "?page=1&mode=menu&filtr=front",
                data={
                    "form3": "",
                    "date": "2026-04-20",
                },
            )

        assert response.status_code == 302
        assert getattr(response, "url") == path + "?page=1&mode=menu&filtr=front"

        outline.refresh_from_db()
        assert outline.date == date(2026, 4, 20)
        assert called_with == [outline.pk]
