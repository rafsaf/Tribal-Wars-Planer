from base.models.message import Message
from base.models.profile import Profile
from base.models import Server, World
from django.contrib.auth.models import User


def test_server_signal_post_create_new_test_world():
    server = Server.objects.create(
        dns="testserver",
        prefix="te",
    )
    assert World.objects.filter(postfix="Test", server=server).exists()


def test_message_signal_update_profiles():
    user = User.objects.create(
        username="test_user", password="test_pass", email="email@email.com"
    )
    profile: Profile = Profile.objects.get(user=user)
    assert profile.messages == 0
    Message.objects.create(text="aaa")
    profile.refresh_from_db()
    assert profile.messages == 1


def test_post_create_user_create_new_profile():
    user = User.objects.create(
        username="test_user", password="test_pass", email="email@email.com"
    )
    assert Profile.objects.filter(user=user).exists()
