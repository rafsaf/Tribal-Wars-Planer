from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from base.models import Profile


def create_user(username: str, password: str) -> None:
    User.objects.bulk_create(
        [
            User(
                username=username,
                email="sample@email.co.uk",
                password=make_password(password),
                is_active=True,
            )
        ]
    )
    user = User.objects.get(username=username)
    Profile.objects.create(user=user)
