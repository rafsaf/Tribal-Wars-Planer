# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
