from prometheus_client import Counter, Summary


REQUEST_LATENCY = Summary(
    "request_latency_seconds", "Latency of request for view", ["view_name", "method"]
)

REQUEST_COUNT = Counter(
    "request_count", "Number of requests for view", ["view_name", "method"]
)

REQUEST_TOTAL = Counter("request_total", "Total number of requests")
