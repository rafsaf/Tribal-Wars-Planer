from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "base"

    def ready(self) -> None:
        from base import signals

        return super().ready()
