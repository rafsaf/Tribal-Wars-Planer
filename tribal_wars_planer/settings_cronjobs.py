# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import os

from tribal_wars_planer.settings import *  # noqa

JOB_MIN_INTERVAL = int(os.environ.get("JOB_MIN_INTERVAL", 10))
JOB_MAX_INTERVAL = int(os.environ.get("JOB_MAX_INTERVAL", 15))
assert JOB_MAX_INTERVAL >= JOB_MIN_INTERVAL
JOB_LIFETIME_MAX_SECS = int(os.environ.get("JOB_LIFETIME_MAX_SECS", 0))
assert JOB_LIFETIME_MAX_SECS == 0 or JOB_LIFETIME_MAX_SECS >= 120

INSTALLED_APPS = [
    "base",
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/cronjobs.log",
            "formatter": "verbose",
            "level": "INFO",
        },
        "stream": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["file", "stream"],
        },
    },
}
