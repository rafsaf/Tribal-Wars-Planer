from time import time
from typing import Callable

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import resolve

import metrics


def PrometheusBeforeMiddleware(get_response: Callable):
    def middleware(request: HttpRequest):

        if "/api/metrics/" not in request.path:
            metrics.REQUEST_TOTAL.inc()
            setattr(request, "_metrics_process_time_start", time())

        response = get_response(request)

        return response

    return middleware


def PrometheusAfterMiddleware(get_response: Callable):
    def middleware(request: HttpRequest):
        match = resolve(request.path)

        if "metrics_export" in match.view_name:
            response: HttpResponse = get_response(request)

        else:
            metrics.REQUEST_COUNT.labels(
                view_name=match.view_name, method=request.method
            ).inc()
            response: HttpResponse = get_response(request)
            metrics.REQUEST_LATENCY.labels(
                view_name=match.view_name, method=request.method
            ).observe(time() - getattr(request, "_metrics_process_time_start"))

        return response

    return middleware
