# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import logging
import zoneinfo
from collections.abc import Callable
from time import time
from typing import Any

from django.contrib.auth import logout as auth_logout
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils import timezone

import metrics
from base.models.profile import Profile

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


def UserDeletedMiddleware(get_response: Callable) -> Callable[..., Any]:
    def middleware(request: HttpRequest) -> Any:

        if request.user.is_authenticated:
            try:
                profile = request.user.profile  # type: ignore
            except Profile.DoesNotExist:
                log.error("profile should already exists")
            else:
                if profile.deleted_at is not None:
                    auth_logout(request)
                    return redirect(reverse("base:account_removed"))

        response = get_response(request)

        return response

    return middleware
