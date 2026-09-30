# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
