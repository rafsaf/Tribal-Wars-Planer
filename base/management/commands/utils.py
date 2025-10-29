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

import threading
from collections.abc import Callable
from logging import Logger
from time import time

from django import db
from django.core.management.base import BaseCommand

import metrics


def db_conn_clean_wrapper(job_func: Callable[[], None]):
    def wrapper(*args, **kwargs) -> None:
        db.close_old_connections()
        try:
            job_func(*args, **kwargs)
        finally:
            db.close_old_connections()

    return wrapper


def run_threaded(job_func: Callable[[], None], **kwargs) -> None:
    job_thread = threading.Thread(target=db_conn_clean_wrapper(job_func), kwargs=kwargs)
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
                raise
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
