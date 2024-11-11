# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
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

import logging
import zoneinfo
from collections.abc import Callable
from time import time
from typing import Any

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import resolve
from django.utils import timezone

import metrics

log = logging.getLogger(__name__)


def PrometheusBeforeMiddleware(get_response: Callable) -> Callable[..., Any]:
    def middleware(request: HttpRequest) -> Any:
        setattr(request, "_metrics_process_time_start", time())
        response = get_response(request)

        return response

    return middleware


def PrometheusAfterMiddleware(
    get_response: Callable,
) -> Callable[..., Any | HttpResponse]:
    def middleware(request: HttpRequest) -> Any | HttpResponse:
        match = resolve(request.path)

        metrics.REQUEST_COUNT.labels(
            view_name=match.view_name, method=request.method
        ).inc()
        response: HttpResponse = get_response(request)

        if response.status_code >= 500:
            metrics.ERRORS.labels(f"{match.view_name} {response.status_code}").inc()

        metrics.REQUEST_LATENCY.labels(
            view_name=match.view_name, method=request.method
        ).observe(time() - getattr(request, "_metrics_process_time_start"))

        return response

    return middleware


def TimezoneMiddleware(get_response: Callable) -> Callable[..., Any]:
    def middleware(request: HttpRequest) -> Any:
        tz = request.COOKIES.get("mytz")
        if tz:
            timezone.activate(zoneinfo.ZoneInfo(tz))
        else:
            timezone.activate(zoneinfo.ZoneInfo("UTC"))
        response = get_response(request)

        return response

    return middleware
