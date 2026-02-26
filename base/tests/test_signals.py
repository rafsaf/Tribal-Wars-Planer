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

from django.contrib.auth.models import User

from base.models import Server, World
from base.models.profile import Profile


def test_server_signal_post_create_new_test_world():
    server = Server.objects.create(
        dns="testserver",
        prefix="te",
    )
    assert World.objects.filter(postfix="Test", server=server).exists()


def test_post_create_user_create_new_profile():
    user = User.objects.create(
        username="test_user", password="test_pass", email="email@email.com"
    )
    assert Profile.objects.filter(user=user).exists()
