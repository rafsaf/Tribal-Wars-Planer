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

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from base.models import Profile


def create_user(username: str, password: str, is_superuser: bool = False) -> User:
    User.objects.bulk_create(
        [
            User(
                username=username,
                email="sample@email.co.uk",
                password=make_password(password),
                is_active=True,
                is_superuser=is_superuser,
            )
        ]
    )
    user = User.objects.get(username=username)
    Profile.objects.create(user=user)
    return user
