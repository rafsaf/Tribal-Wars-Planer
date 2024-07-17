# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
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

import sys
import threading
from collections.abc import Callable
from logging import Logger
from time import time

from django.core.management.base import BaseCommand

import metrics


def run_threaded(job_func: Callable[[], None], **kwargs):
    #  2003  sudo apt-get install -y net-tools
    #  2004  sudo nsenter -t 57346 -n netstat
    #  2005  sudo nsenter -t 57346 -n netstat > txt
    #  2006  ps aux | grep manage
    #  2007  sudo nsenter -t 59132 -n netstat > txt
    job_thread = threading.Thread(target=job_func, kwargs=kwargs)
    job_thread.start()


def job_logs_and_metrics(log: Logger):
    def outer_wrapper(function):
        def inner_wrapper(self: BaseCommand, *args, **kwargs):
            task_name = log.name.split(".")[-1]
            self.stdout.write(self.style.SUCCESS(f"starting task {task_name}"))
            log.info(f"starting task {task_name}")
            start = time()
            try:
                result = function(self, *args, **kwargs)
            except Exception as error:
                log.error(f"error in task {task_name}: {error}")
                self.stdout.write(str(error))
                self.stdout.write(self.style.ERROR(f"task {task_name} fail"))
                metrics.ERRORS.labels(f"task_{task_name}").inc()
                sys.exit(1)
            else:
                metrics.CRONTASK.labels(task_name).inc()
                success_msg = (
                    f"success task {task_name} - processed in {time() - start}s"
                )
                log.info(success_msg)
                self.stdout.write(self.style.SUCCESS(success_msg))
                return result

        return inner_wrapper

    return outer_wrapper
