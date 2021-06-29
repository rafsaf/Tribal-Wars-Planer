from django.db import connection
from functools import reduce
from time import time
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from operator import add


class StatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:

        before_queries: int = len(connection.queries)
        start: float = time()

        response: HttpResponse = self.get_response(request)
        if response.headers.get("Content-Type") == "text/html; charset=utf-8":
            total_time: float = time() - start

            db_queries: int = len(connection.queries) - before_queries
            if db_queries > 0:
                db_time: float = reduce(
                    add, [float(q["time"]) for q in connection.queries[before_queries:]]
                )
            else:
                db_time: float = 0.0

            python_time: float = total_time - db_time

            response.content = (
                f"<!--\r\n Total time: {total_time}s\r\n Python time: {python_time}s\r\n DB time: {db_time}s\r\n-->".encode(
                    "utf-8"
                )
                + response.content
            )
        return response
