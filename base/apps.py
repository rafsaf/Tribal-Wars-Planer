from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "base"

    def ready(self) -> None:
        import base.signals  # noqa: F401

        return super().ready()
