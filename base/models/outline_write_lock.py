# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from enum import StrEnum

from django.db import models

from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class OutlineWriteLock(models.Model):
    class LOCK_NAME_TYPES(StrEnum):
        WRITE_OUTLINE = "write_outline"
        CREATE_WEIGHTMAX = "create_weightmax_objects"

    outline_id = models.BigIntegerField(db_index=True)
    lock_name = models.CharField(max_length=64)
    lock_expire = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FetchErrorManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["outline_id", "lock_name"],
                name="unique_lock_by_outline_and_name",
            )
        ]
