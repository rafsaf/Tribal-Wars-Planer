from prometheus_client import Counter, Gauge, Summary

REQUEST_LATENCY = Summary(
    "request_latency_seconds", "Latency of request for view", ["view_name", "method"]
)

REQUEST_COUNT = Counter(
    "request_count", "Number of requests for view", ["view_name", "method"]
)

ERRORS = Counter("errors", "App errors", ["error_messsage"])

DBUPDATE = Counter(
    "database_update",
    "Village, Player, Tribe updates",
    ["table_name", "world", "action"],
)
CRONTASK = Counter("cron_task", "Cron tasks", ["job_name"])

WORLD_LAST_UPDATE = Gauge("world_last_update", "Game world last update", ["world"])

MEMORY = Gauge("memory", "Memory usage percent")

DISK = Gauge("disk", "Disk usage percent")

CPU = Gauge("cpu", "CPU usage percent")
