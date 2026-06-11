# Copyright 2026 Rafał Safin (rafsaf). All Rights Reserved.
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

import json
import logging
from time import time
from typing import NotRequired, TypedDict

import requests
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

log = logging.getLogger(__name__)

PLAUSIBLE_SCRIPT_CACHE_KEY = "public-plausible-script"
PLAUSIBLE_SCRIPT_SOFT_TIMEOUT = 60 * 60
PLAUSIBLE_SCRIPT_RESPONSE_CACHE_TIMEOUT = 60 * 60
PLAUSIBLE_PROXY_SCRIPT_PATH = "/api/public/analytics/plausible/script.js"


class PlausibleScriptCachePayload(TypedDict):
    content: bytes
    content_type: str
    refreshed_at: NotRequired[float]


def get_plausible_frontend_config() -> dict[str, bool | str]:
    is_enabled = bool(settings.PLAUSIBLE_DOMAIN and settings.PLAUSIBLE_SCRIPT_PATH)
    endpoint = ""
    if is_enabled:
        endpoint = f"{settings.PLAUSIBLE_DOMAIN.rstrip('/')}/api/event"

    return {
        "enabled": is_enabled,
        "endpoint": endpoint,
        "captureOnLocalhost": settings.PLAUSIBLE_CAPTURE_ON_LOCALHOST,
        "scriptSrc": PLAUSIBLE_PROXY_SCRIPT_PATH if is_enabled else "",
    }


def _render_javascript_response(
    content: str | bytes,
    *,
    cache_control: str,
    content_type: str = "application/javascript; charset=utf-8",
    status: int = 200,
) -> HttpResponse:
    response = HttpResponse(content, content_type=content_type, status=status)
    response["Cache-Control"] = cache_control
    return response


@require_GET
def plausible_config_script(request: HttpRequest) -> HttpResponse:
    response = render(
        request,
        "base/plausible_config.js",
        {
            "plausible_config_json": json.dumps(
                get_plausible_frontend_config(), separators=(",", ":")
            )
        },
        content_type="application/javascript; charset=utf-8",
    )
    response["Cache-Control"] = "public, max-age=300"
    return response


def _fetch_remote_plausible_script() -> tuple[bytes, str]:
    upstream_url = (
        f"{settings.PLAUSIBLE_DOMAIN.rstrip('/')}{settings.PLAUSIBLE_SCRIPT_PATH}"
    )
    upstream_response = requests.get(upstream_url, timeout=(3.05, 10))
    upstream_response.raise_for_status()

    upstream_content_type = upstream_response.headers.get(
        "Content-Type", "application/javascript; charset=utf-8"
    )
    return upstream_response.content, upstream_content_type


def get_cached_plausible_script() -> PlausibleScriptCachePayload | None:
    cached_payload = cache.get(PLAUSIBLE_SCRIPT_CACHE_KEY)
    if not isinstance(cached_payload, dict):
        return None
    if "content" not in cached_payload or "content_type" not in cached_payload:
        return None
    content = cached_payload["content"]
    content_type = cached_payload["content_type"]
    if not isinstance(content, bytes) or not isinstance(content_type, str):
        return None

    refreshed_at = cached_payload.get("refreshed_at")
    payload: PlausibleScriptCachePayload = {
        "content": content,
        "content_type": content_type,
    }
    if isinstance(refreshed_at, (int, float)):
        payload["refreshed_at"] = float(refreshed_at)
    return payload


def is_plausible_script_refresh_due(
    cached_payload: PlausibleScriptCachePayload | None,
) -> bool:
    if cached_payload is None:
        return True

    refreshed_at = cached_payload.get("refreshed_at")
    if not isinstance(refreshed_at, (int, float)):
        return True

    return time() - refreshed_at >= PLAUSIBLE_SCRIPT_SOFT_TIMEOUT


def cache_plausible_script(script_content: bytes, content_type: str) -> None:
    cache.set(
        PLAUSIBLE_SCRIPT_CACHE_KEY,
        {
            "content": script_content,
            "content_type": content_type,
            "refreshed_at": time(),
        },
        timeout=None,
    )


def refresh_plausible_script_cache(*, force: bool = False) -> bool:
    cached_payload = get_cached_plausible_script()
    if not force and not is_plausible_script_refresh_due(cached_payload):
        return False

    script_content, content_type = _fetch_remote_plausible_script()
    cache_plausible_script(script_content, content_type)
    return True


@require_GET
def plausible_proxy_script(request: HttpRequest) -> HttpResponse:
    if not settings.PLAUSIBLE_DOMAIN or not settings.PLAUSIBLE_SCRIPT_PATH:
        return _render_javascript_response(
            "",
            cache_control="no-store, max-age=0",
            status=404,
        )

    cached_payload = get_cached_plausible_script()
    if cached_payload is not None:
        return _render_javascript_response(
            cached_payload["content"],
            cache_control=f"public, max-age={PLAUSIBLE_SCRIPT_RESPONSE_CACHE_TIMEOUT}",
            content_type=cached_payload["content_type"],
        )

    log.warning("Plausible script cache is empty")
    return _render_javascript_response(
        "",
        cache_control="no-store, max-age=0",
        status=502,
    )
