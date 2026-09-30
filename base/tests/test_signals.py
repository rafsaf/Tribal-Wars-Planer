# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
