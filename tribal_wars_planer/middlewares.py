from django.db import connection
from functools import reduce
from time import time
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from operator import add


class StatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_time: float = 0.0
        self.python_time: float = 0.0
        self.db_time: float = 0.0
        self.db_queries: int = 0

    def __call__(self, request):

        before_queries: int = len(connection.queries)
        start: float = time()

        response: HttpResponse = self.get_response(request)
        if response.headers["Content-Type"] == "text/html; charset=utf-8":
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

    def process_template_response(self, request, response: TemplateResponse):
        if response.context_data is None:
            response.context_data = {}
        print(response.context_data)
        response.context_data["stats_total_time"] = self.total_time
        response.context_data["stats_python_time"] = self.python_time
        response.context_data["stats_db_time"] = self.db_time
        response.context_data["stats_db_queries"] = self.db_queries
        return response
