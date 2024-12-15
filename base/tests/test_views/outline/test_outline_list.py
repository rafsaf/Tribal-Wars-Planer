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

import datetime

from django.urls import reverse

from base.models import Outline
from base.models.result import Result
from base.tests.test_utils.mini_setup import MiniSetup


class OutlineList(MiniSetup):
    def test_planer___302_not_auth_redirect_login(self):
        PATH = reverse("base:planer")

        response = self.client.get(PATH)
        assert response.status_code == 302
        assert getattr(response, "url") == self.login_page_path(next=PATH)

    def test_planer___200_foreign_user_works_ok(self):
        self.login_foreign_user()
        PATH = reverse("base:planer")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer___200_auth_works_ok(self):
        PATH = reverse("base:planer")

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_planer___200_auth_remove_editable_outline_leave_foreign_outline(self):
        PATH = reverse("base:planer")
        self.create_foreign_outline()
        self.get_outline()
        self.login_me()
        assert Outline.objects.count() == 2
        response = self.client.get(PATH)
        assert response.status_code == 200
        query = response.context["outlines"]
        assert len(query) == 0
        assert Outline.objects.count() == 1

    def test_planer___200_auth_show_active_outline(self):
        PATH = reverse("base:planer")
        outline = self.get_outline()
        outline.status = "active"
        outline.editable = "inactive"
        outline.save()

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        query = response.context["outlines"]
        assert len(query) == 1
        assert Outline.objects.count() == 1

    def test_planer___200_auth_not_show_inactive_outline(self):
        PATH = reverse("base:planer") + "?show-hidden=false"
        outline = self.get_outline()
        outline.status = "inactive"
        outline.editable = "inactive"
        outline.save()

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        query = response.context["outlines"]
        assert len(query) == 0
        assert Outline.objects.count() == 1

    def test_planer___200_auth_show_inactive_outline_with_show_hidden(self):
        PATH = reverse("base:planer") + "?show-hidden=true"
        outline = self.get_outline()
        outline.status = "inactive"
        outline.editable = "inactive"
        outline.save()

        self.login_me()
        response = self.client.get(PATH)
        assert response.status_code == 200
        query = response.context["outlines"]
        assert len(query) == 1
        assert Outline.objects.count() == 1

    def test_planer___404_duplicate_form_not_work_for_foreign_user(self):
        PATH = reverse("base:planer")
        outline = self.get_outline(editable="inactive")
        outline.save()

        self.login_foreign_user()
        response = self.client.post(
            PATH,
            data={
                "form1": "",
                "name": "name123",
                "date": datetime.date.today(),
                "parent_outline": str(outline.pk),
                "unused_troops": "on",
            },
        )
        assert response.status_code == 404

    def test_planer___200_duplicate_form_creates_new_outline(self):
        PATH = reverse("base:planer")
        outline = self.get_outline(editable="inactive", add_result=True)
        outline.save()

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form1": "",
                "name": "name123_duplicate",
                "date": datetime.date.today(),
                "parent_outline": str(outline.pk),
                "unused_troops": "on",
            },
        )
        assert response.status_code == 302

        response = self.client.get(PATH)
        assert response.status_code == 200

        query = response.context["outlines"]
        assert len(query) == 2
        assert Outline.objects.count() == 2

        assert Outline.objects.filter(name="name123_duplicate").exists()

    def test_planer___302_duplicate_form_properly_use_off_troops(self):
        PATH = reverse("base:planer")
        outline = self.get_outline(editable="inactive", add_result=True)
        outline.input_data_type = Outline.ARMY_COLLECTION
        outline.off_troops = "abcd"
        outline.save()
        hash = outline.get_or_set_off_troops_hash(force_recalculate=True)
        result: Result = outline.result  # type: ignore
        result.results_export = "xyzc"
        result.save()

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form1": "",
                "name": "name123_duplicate",
                "date": datetime.date.today(),
                "parent_outline": str(outline.pk),
                "unused_troops": "on",
            },
        )
        assert response.status_code == 302

        assert Outline.objects.count() == 2
        new = Outline.objects.get(name="name123_duplicate")

        assert new.off_troops == result.results_export
        assert new.off_troops_hash != hash

    def test_planer___302_duplicate_form_empty_off_deff_troops_without_unused_troops(
        self,
    ):
        PATH = reverse("base:planer")
        outline = self.get_outline(editable="inactive", add_result=True)
        outline.input_data_type = Outline.DEFF_COLLECTION
        outline.deff_troops = "abcd"
        outline.off_troops = "abcd"
        outline.save()
        outline.get_or_set_off_troops_hash(force_recalculate=True)
        outline.get_or_set_deff_troops_hash(force_recalculate=True)
        result: Result = outline.result  # type: ignore
        result.results_export = "xyzc"
        result.save()

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form1": "",
                "name": "name123_duplicate",
                "date": datetime.date.today(),
                "parent_outline": str(outline.pk),
            },
        )
        assert response.status_code == 302

        assert Outline.objects.count() == 2
        new = Outline.objects.get(name="name123_duplicate")

        assert new.off_troops == ""
        assert new.deff_troops == ""
        assert new.off_troops_hash == ""
        assert new.deff_troops_hash == ""

    def test_planer___200_duplicate_form_invalid_payload_no_name(
        self,
    ):
        PATH = reverse("base:planer")
        outline = self.get_outline(editable="inactive", add_result=True)

        self.login_me()
        response = self.client.post(
            PATH,
            data={
                "form1": "",
                "date": datetime.date.today(),
                "parent_outline": str(outline.pk),
            },
        )
        assert response.status_code == 200

        assert Outline.objects.count() == 1
        context_outline = response.context["outlines"][0]
        form = getattr(context_outline, "duplicate_form")
        assert form.errors is not None
