import logging
from typing import Any

from django.db.models import Manager, Model
from django.db.models.fetch_modes import FetchOne

log = logging.getLogger(__name__)


class FetchError(FetchOne):
    __slots__ = ()

    track_peers = False

    def fetch(self, fetcher: Any, instance: Model) -> None:
        klass = instance.__class__.__qualname__
        field_name = fetcher.field.name
        log.error("Fetching of %s.%s blocked.", klass, field_name, stack_info=True)
        return super().fetch(fetcher, instance)

    def __reduce__(self):
        return "FETCH_ERROR"


FETCH_ERROR = FetchError()


class FetchErrorManager(Manager):
    def get_queryset(self):
        return super().get_queryset().fetch_mode(FETCH_ERROR)
