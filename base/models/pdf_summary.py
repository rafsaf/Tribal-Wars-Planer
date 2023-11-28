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

import os

from django.conf import settings
from django.db import models


class PDFPaymentSummary(models.Model):
    period = models.CharField(max_length=10)
    path = models.CharField(max_length=300, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PDF Summary"
        verbose_name_plural = "PDF Summaries"

    def delete(self) -> tuple[int, dict[str, int]]:
        try:
            os.remove(f"{settings.MEDIA_ROOT}/{self.path}")
        except FileNotFoundError:
            pass

        return super().delete()

    def url(self) -> str:
        return f"{settings.MEDIA_URL}{self.path}"
