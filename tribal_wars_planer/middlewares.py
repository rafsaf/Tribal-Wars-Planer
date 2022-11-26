import logging
from collections.abc import Callable
from time import time

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import resolve

import metrics

log = logging.getLogger(__name__)


def PrometheusBeforeMiddleware(get_response: Callable):
    def middleware(request: HttpRequest):
        setattr(request, "_metrics_process_time_start", time())
        response = get_response(request)

        return response

    return middleware


def PrometheusAfterMiddleware(get_response: Callable):
    def middleware(request: HttpRequest):
        match = resolve(request.path)

        metrics.REQUEST_COUNT.labels(
            view_name=match.view_name, method=request.method
        ).inc()
        response: HttpResponse = get_response(request)

        if response.status_code >= 400:
            metrics.ERRORS.labels(f"{match.view_name} {response.status_code}").inc()

        metrics.REQUEST_LATENCY.labels(
            view_name=match.view_name, method=request.method
        ).observe(time() - getattr(request, "_metrics_process_time_start"))

        return response

    return middleware
