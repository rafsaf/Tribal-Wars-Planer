import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def plausible_settings(settings):
    settings.PLAUSIBLE_DOMAIN = "https://plausible.example.com"
    settings.PLAUSIBLE_SCRIPT_PATH = "/js/script.js"
    settings.PLAUSIBLE_CAPTURE_ON_LOCALHOST = True
    return settings


def test_config_script_contains_runtime_frontend_config(client, plausible_settings):
    response = client.get(reverse("public_plausible_config_script"))

    assert response.status_code == 200
    assert response["Content-Type"] == "application/javascript; charset=utf-8"
    assert response["Cache-Control"] == "public, max-age=300"
    content = response.content.decode()
    assert "window.twpPlausibleConfig = JSON.parse(" in content
    assert "\\u0022enabled\\u0022:true" in content
    assert (
        "\\u0022scriptSrc\\u0022:\\u0022/api/public/analytics/plausible/script.js\\u0022"
        in content
    )
    assert (
        "\\u0022endpoint\\u0022:\\u0022https://plausible.example.com/api/event\\u0022"
        in content
    )
    assert "\\u0022captureOnLocalhost\\u0022:true" in content
    assert "bootstrapTwpPlausible" in content


def test_proxy_script_serves_cached_response_without_upstream_fetch(
    client, monkeypatch: pytest.MonkeyPatch, plausible_settings
):
    from base.views import analytics

    monkeypatch.setattr(
        analytics.cache,
        "get",
        lambda key: {
            "content": b"console.log('plausible');",
            "content_type": "application/javascript",
            "refreshed_at": 1.0,
        },
    )
    monkeypatch.setattr(
        analytics.requests,
        "get",
        lambda *args, **kwargs: pytest.fail(
            "request-time upstream fetch should not run"
        ),
    )

    response = client.get(reverse("public_plausible_proxy_script"))
    second_response = client.get(reverse("public_plausible_proxy_script"))

    assert response.status_code == 200
    assert response.content == b"console.log('plausible');"
    assert response["Content-Type"] == "application/javascript"
    assert response["Cache-Control"] == "public, max-age=3600"
    assert second_response.status_code == 200
    assert second_response.content == b"console.log('plausible');"
    assert second_response["Cache-Control"] == "public, max-age=3600"


def test_proxy_script_returns_404_when_analytics_disabled(client, settings):
    settings.PLAUSIBLE_DOMAIN = ""
    settings.PLAUSIBLE_SCRIPT_PATH = ""

    response = client.get(reverse("public_plausible_proxy_script"))

    assert response.status_code == 404


def test_proxy_script_returns_bad_gateway_when_cache_is_empty(
    client, monkeypatch: pytest.MonkeyPatch, plausible_settings
):
    from base.views import analytics

    monkeypatch.setattr(analytics.cache, "get", lambda key: None)
    monkeypatch.setattr(
        analytics.requests,
        "get",
        lambda *args, **kwargs: pytest.fail(
            "request-time upstream fetch should not run"
        ),
    )

    response = client.get(reverse("public_plausible_proxy_script"))

    assert response.status_code == 502
