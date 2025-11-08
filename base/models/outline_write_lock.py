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

from enum import StrEnum

from django.db import models


class OutlineWriteLock(models.Model):
    class LOCK_NAME_TYPES(StrEnum):
        WRITE_OUTLINE = "write_outline"
        CREATE_WEIGHTMAX = "create_weightmax_objects"

    outline_id = models.BigIntegerField(db_index=True)
    lock_name = models.CharField(max_length=64)
    lock_expire = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["outline_id", "lock_name"],
                name="unique_lock_by_outline_and_name",
            )
        ]
