import threading
from logging import Logger
from time import time
from typing import Callable

from django.core.management.base import BaseCommand

import metrics


def run_threaded(job_func: Callable[[], None], **kwargs):
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
                exit(1)
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
