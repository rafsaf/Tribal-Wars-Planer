import inspect
import logging
from typing import Any

from django.conf import settings
from django.db.models import Manager, Model
from django.db.models.fetch_modes import FetchOne

log = logging.getLogger(__name__)


class FetchError(FetchOne):
    __slots__ = ()

    track_peers = False

    def fetch(self, fetcher: Any, instance: Model) -> None:
        klass = instance.__class__.__qualname__
        field_name = fetcher.field.name

        if not settings.TESTING and not self._is_django_admin_call():
            log.error("Unexpected fetch of %s.%s.", klass, field_name, stack_info=True)

        return super().fetch(fetcher, instance)

    def _is_django_admin_call(self) -> bool:
        # Walk frame back pointers directly to avoid inspect.stack shadowing issues
        frame = inspect.currentframe()
        try:
            depth = 0
            while frame and depth < 20:
                module_name = frame.f_globals.get("__name__", "")
                if module_name.startswith("django.contrib.admin"):
                    return True
                frame = frame.f_back
                depth += 1
        finally:
            del frame  # Avoid reference cycle retention
        return False

    def __reduce__(self):
        return "FETCH_ERROR"


FETCH_ERROR = FetchError()


class FetchErrorManager(Manager):
    def get_queryset(self):
        return super().get_queryset().fetch_mode(FETCH_ERROR)
