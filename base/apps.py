# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "base"

    def ready(self) -> None:
        import base.signals  # noqa: F401

        return super().ready()
