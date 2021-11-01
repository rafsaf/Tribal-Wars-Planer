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

from django.urls import reverse
from base.tests.test_utils.create_user import create_user
from random import randint
from base.tests.test_utils.mini_setup import MiniSetup


class PaymentSumUpView(MiniSetup):
    def test_payment_summary___302_not_auth_redirect_login(self):
        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)

        assert response.status_code == 302
        assert response.url == self.login_page_path(next=PATH)

    def test_payment_summary___404_foreign_user(self):
        self.login_foreign_user()
        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_payment_summary___404_me(self):
        self.login_me()
        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_payment_summary___404_superuser(self):
        username = "some_superuser"
        password = "password123"
        create_user(username, password, is_superuser=True)
        self.client.login(username=username, password=password)

        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)
        assert response.status_code == 404

    def test_payment_summary___200_superuser_and_admin(self):
        username = "admin"
        password = "password123"
        create_user(username, password, is_superuser=True)
        self.client.login(username=username, password=password)

        PATH = reverse("base:payment_summary")

        response = self.client.get(PATH)
        assert response.status_code == 200

    def test_payment_summary___302_post_superuser_and_admin(self):
        username = "admin"
        password = "password123"
        create_user(username, password, is_superuser=True)
        self.client.login(username=username, password=password)
        for _ in range(100):
            self.create_random_payment()

        PATH = reverse("base:payment_summary")

        response = self.client.post(PATH, {"form": ""})
        assert response.status_code == 302
