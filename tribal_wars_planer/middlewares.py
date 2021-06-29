from time import time
from django.http import HttpRequest
from django.http.response import HttpResponse


class StatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start: float = time()
        response: HttpResponse = self.get_response(request)
        if response.headers.get("Content-Type") == "text/html; charset=utf-8":
            total_time: float = time() - start
            response.content = (
                f"<!--\r\n Rendered with Django 3.2.4\r\n Total time: {total_time}s\r\n-->".encode(
                    "utf-8"
                )
                + response.content
            )
        return response
