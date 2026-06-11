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
from time import time

import pytest
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone
from freezegun import freeze_time

from base.models import Outline, OutlineOverview, Overview, Payment, Server, World
from base.tests.test_utils.create_user import create_user
from base.views import analytics
from utils.database_update import WorldUpdateHandler


def test_create_servers_command() -> None:
    call_command("createservers")

    assert Server.objects.all().count() == len(settings.TRIBAL_WARS_SUPPORTED_SERVERS)

    for server in Server.objects.all():
        worlds: list[World] = list(World.objects.filter(server=server))
        assert len(worlds) == 1
        assert worlds[0].postfix == "Test"


def test_orphanedoutlineoverviewsdelete_no_delete_with_outline() -> None:
    Server.objects.create(
        dns="testserver",
        prefix="te",
    )
    world = World.objects.get(postfix="Test")
    outline = Outline.objects.create(
        name="",
        date=datetime.date.today(),
        world=world,
        owner=create_user("user", "password"),
    )
    OutlineOverview.objects.create(outline=outline)

    call_command("orphanedoutlineoverviewsdelete")

    assert OutlineOverview.objects.count() == 1


def test_orphanedoutlineoverviewsdelete_no_delete_with_overview() -> None:
    outline_overview = OutlineOverview.objects.create(outline=None)
    Overview.objects.create(
        outline_overview=outline_overview,
        outline=None,
        player="xxxx",
        token="abcd",
        table="xxxx",
        string="xxxx",
        deputy="xxxx",
        extended="xxxx",
    )

    call_command("orphanedoutlineoverviewsdelete")

    assert OutlineOverview.objects.count() == 1


def test_orphanedoutlineoverviewsdelete_delete() -> None:
    OutlineOverview.objects.create(outline=None)

    call_command("orphanedoutlineoverviewsdelete")

    assert OutlineOverview.objects.count() == 0


@pytest.mark.parametrize(
    "send_mail,mail_sent,user,mail_send_after",
    [
        (False, False, False, False),
        (True, True, False, True),
        (True, False, False, False),
        (False, True, False, True),
        (True, True, True, True),
        (True, False, True, True),
    ],
)
def test_missedemailssend_no_delete_with_overview(
    send_mail: bool, mail_sent: bool, user: bool, mail_send_after: bool
) -> None:
    user_acc = create_user("user", "password")

    payment = Payment.objects.create(
        amount=1,
        event_id="x",
        payment_date=datetime.date(2024, 10, 12),
        send_mail=send_mail,
        mail_sent=mail_sent,
        user=user_acc if user else None,
    )

    call_command("missedemailssend")

    payment.refresh_from_db()
    assert payment.mail_sent == mail_send_after


@freeze_time("2026-06-10 12:00:00")
def test_inactiveusersdelete_deletes_only_inactive_users_older_than_24_hours() -> None:
    current_time = timezone.now()

    old_inactive_user = User.objects.create_user(
        username="old_inactive_user",
        email="old_inactive_user@example.com",
        password="password",
        is_active=False,
    )
    recent_inactive_user = User.objects.create_user(
        username="recent_inactive_user",
        email="recent_inactive_user@example.com",
        password="password",
        is_active=False,
    )
    old_active_user = User.objects.create_user(
        username="old_active_user",
        email="old_active_user@example.com",
        password="password",
        is_active=True,
    )

    User.objects.filter(pk=old_inactive_user.pk).update(
        date_joined=current_time - datetime.timedelta(hours=24, seconds=1)
    )
    User.objects.filter(pk=recent_inactive_user.pk).update(
        date_joined=current_time - datetime.timedelta(hours=23, minutes=59, seconds=59)
    )
    User.objects.filter(pk=old_active_user.pk).update(
        date_joined=current_time - datetime.timedelta(hours=24, seconds=1)
    )

    call_command("inactiveusersdelete")

    assert not User.objects.filter(pk=old_inactive_user.pk).exists()
    assert User.objects.filter(pk=recent_inactive_user.pk).exists()
    assert User.objects.filter(pk=old_active_user.pk).exists()


def test_updateworldsconfiguration(monkeypatch: pytest.MonkeyPatch) -> None:
    server = Server.objects.create(
        dns="testserver",
        prefix="te",
    )
    world = World.objects.create(
        server=server,
        postfix="1",
        paladin="inactive",
        archer="inactive",
        militia="active",
    )

    def fake_config_update(*args) -> None:
        world.archer = "active"
        world.save()

    monkeypatch.setattr(
        WorldUpdateHandler, "create_or_update_config", fake_config_update
    )

    call_command("updateworldsconfiguration")

    world.refresh_from_db()
    assert world.archer == "active"


def test_refreshplausiblescriptcache_updates_cache(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings.PLAUSIBLE_DOMAIN = "https://plausible.example.com"
    settings.PLAUSIBLE_SCRIPT_PATH = "/js/script.js"

    class FakeResponse:
        content = b"console.log('plausible');"
        headers = {"Content-Type": "application/javascript"}

        def raise_for_status(self) -> None:
            return None

    cache_items: dict[str, dict[str, bytes | str | float]] = {}
    cache_timeouts: list[int | None] = []
    request_calls: list[tuple[str, tuple[float, int]]] = []

    def fake_get(url: str, timeout: tuple[float, int]) -> FakeResponse:
        request_calls.append((url, timeout))
        return FakeResponse()

    monkeypatch.setattr(analytics.requests, "get", fake_get)
    monkeypatch.setattr(analytics.cache, "get", cache_items.get)

    def fake_cache_set(key, value, timeout) -> None:
        cache_items[key] = value
        cache_timeouts.append(timeout)

    monkeypatch.setattr(analytics.cache, "set", fake_cache_set)

    call_command("refreshplausiblescriptcache")

    assert request_calls == [("https://plausible.example.com/js/script.js", (3.05, 10))]
    assert cache_timeouts == [None]
    assert cache_items[analytics.PLAUSIBLE_SCRIPT_CACHE_KEY]["content"] == (
        b"console.log('plausible');"
    )
    assert (
        cache_items[analytics.PLAUSIBLE_SCRIPT_CACHE_KEY]["content_type"]
        == "application/javascript"
    )


def test_refreshplausiblescriptcache_skips_fetch_when_cache_is_fresh(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings.PLAUSIBLE_DOMAIN = "https://plausible.example.com"
    settings.PLAUSIBLE_SCRIPT_PATH = "/js/script.js"

    monkeypatch.setattr(
        analytics.cache,
        "get",
        lambda key: {
            "content": b"console.log('cached');",
            "content_type": "application/javascript",
            "refreshed_at": time(),
        },
    )
    monkeypatch.setattr(
        analytics.requests,
        "get",
        lambda *args, **kwargs: pytest.fail(
            "fresh cache should not trigger upstream fetch"
        ),
    )

    call_command("refreshplausiblescriptcache")


def test_refreshplausiblescriptcache_keeps_stale_cache_when_refresh_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings.PLAUSIBLE_DOMAIN = "https://plausible.example.com"
    settings.PLAUSIBLE_SCRIPT_PATH = "/js/script.js"

    monkeypatch.setattr(
        analytics.cache,
        "get",
        lambda key: {
            "content": b"console.log('cached');",
            "content_type": "application/javascript",
            "refreshed_at": 0.0,
        },
    )
    monkeypatch.setattr(
        analytics.requests,
        "get",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            requests.RequestException("upstream unavailable")
        ),
    )

    call_command("refreshplausiblescriptcache")
