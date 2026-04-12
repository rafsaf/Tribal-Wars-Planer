import pytest
import requests
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


def test_proxy_script_fetches_upstream_and_caches_response(
    client, monkeypatch: pytest.MonkeyPatch, plausible_settings
):
    from base.views import analytics

    class FakeResponse:
        content = b"console.log('plausible');"
        headers = {"Content-Type": "application/javascript"}

        def raise_for_status(self) -> None:
            return None

    cached_items: dict[str, dict[str, bytes | str]] = {}
    request_calls: list[tuple[str, tuple[float, int]]] = []

    def fake_get(url: str, timeout: tuple[float, int]) -> FakeResponse:
        request_calls.append((url, timeout))
        return FakeResponse()

    monkeypatch.setattr(analytics.requests, "get", fake_get)
    monkeypatch.setattr(analytics.cache, "get", cached_items.get)
    monkeypatch.setattr(
        analytics.cache,
        "set",
        lambda key, value, timeout: cached_items.__setitem__(key, value),
    )

    response = client.get(reverse("public_plausible_proxy_script"))
    second_response = client.get(reverse("public_plausible_proxy_script"))

    assert response.status_code == 200
    assert response.content == b"console.log('plausible');"
    assert response["Content-Type"] == "application/javascript"
    assert response["Cache-Control"] == "public, max-age=259200"
    assert second_response.status_code == 200
    assert second_response.content == b"console.log('plausible');"
    assert request_calls == [("https://plausible.example.com/js/script.js", (3.05, 10))]


def test_proxy_script_returns_404_when_analytics_disabled(client, settings):
    settings.PLAUSIBLE_DOMAIN = ""
    settings.PLAUSIBLE_SCRIPT_PATH = ""

    response = client.get(reverse("public_plausible_proxy_script"))

    assert response.status_code == 404


def test_proxy_script_returns_bad_gateway_when_upstream_fails(
    client, monkeypatch: pytest.MonkeyPatch, plausible_settings
):
    from base.views import analytics

    def raise_request_exception(*args, **kwargs):
        raise requests.RequestException("upstream unavailable")

    monkeypatch.setattr(analytics.requests, "get", raise_request_exception)
    monkeypatch.setattr(analytics.cache, "get", lambda key: None)

    response = client.get(reverse("public_plausible_proxy_script"))

    assert response.status_code == 502
