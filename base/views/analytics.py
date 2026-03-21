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

import requests
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

log = logging.getLogger(__name__)

PLAUSIBLE_SCRIPT_CACHE_KEY = "public-plausible-script"
PLAUSIBLE_SCRIPT_CACHE_TIMEOUT = 60 * 60 * 24 * 3
PLAUSIBLE_PROXY_SCRIPT_PATH = "/api/public/analytics/plausible/script.js"


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


@require_GET
def plausible_proxy_script(request: HttpRequest) -> HttpResponse:
    if not settings.PLAUSIBLE_DOMAIN or not settings.PLAUSIBLE_SCRIPT_PATH:
        return _render_javascript_response(
            "",
            cache_control="no-store, max-age=0",
            status=404,
        )

    cached_payload = cache.get(PLAUSIBLE_SCRIPT_CACHE_KEY)
    if cached_payload is not None:
        return _render_javascript_response(
            cached_payload["content"],
            cache_control=f"public, max-age={PLAUSIBLE_SCRIPT_CACHE_TIMEOUT}",
            content_type=cached_payload["content_type"],
        )

    try:
        script_content, content_type = _fetch_remote_plausible_script()
    except requests.RequestException:
        log.exception("Unable to fetch Plausible script from upstream")
        return _render_javascript_response(
            "",
            cache_control="no-store, max-age=0",
            status=502,
        )

    cache.set(
        PLAUSIBLE_SCRIPT_CACHE_KEY,
        {"content": script_content, "content_type": content_type},
        timeout=PLAUSIBLE_SCRIPT_CACHE_TIMEOUT,
    )

    return _render_javascript_response(
        script_content,
        cache_control=f"public, max-age={PLAUSIBLE_SCRIPT_CACHE_TIMEOUT}",
        content_type=content_type,
    )
