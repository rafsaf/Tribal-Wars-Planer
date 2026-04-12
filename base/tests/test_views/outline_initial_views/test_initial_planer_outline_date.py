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
        assert "Edit date" in content
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
