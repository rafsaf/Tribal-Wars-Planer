# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

import os

from django.conf import settings
from django.db import models

from tribal_wars_planer.fetch_error_manager import FetchErrorManager


class PDFPaymentSummary(models.Model):
    period = models.CharField(max_length=10)
    path = models.CharField(max_length=300, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FetchErrorManager()

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
