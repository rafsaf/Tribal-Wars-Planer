from logging import Logger

from django.core.management.base import BaseCommand

import metrics


def job_logs_and_metrics(log: Logger):
    def outer_wrapper(function):
        def inner_wrapper(self: BaseCommand, *args, **kwargs):
            task_name = log.name.split(".")[-1]
            self.stdout.write(self.style.SUCCESS(f"starting task {task_name}"))
            log.info(f"starting task {task_name}")

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
                log.info(f"success task {task_name}")
                self.stdout.write(self.style.SUCCESS(f"success task {task_name}"))
                return result

        return inner_wrapper

    return outer_wrapper
