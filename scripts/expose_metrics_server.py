# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from pathlib import Path
from threading import Event

from dotenv import load_dotenv
from prometheus_client import REGISTRY, start_http_server
from prometheus_client.multiprocess import MultiProcessCollector

BASE_DIR = Path(__file__).resolve().parent.parent


if __name__ == "__main__":
    load_dotenv(dotenv_path=BASE_DIR / ".env")

    MultiProcessCollector(REGISTRY)

    start_http_server(8050)

    Event().wait()
