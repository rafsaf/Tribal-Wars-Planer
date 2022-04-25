import os

from django.conf import settings
from django.db import models


class PDFPaymentSummary(models.Model):
    period = models.CharField(max_length=10)
    path = models.CharField(max_length=300, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self) -> tuple[int, dict[str, int]]:
        try:
            os.remove(f"{settings.MEDIA_ROOT}/{self.path}")
        except FileNotFoundError:
            pass

        return super().delete()

    def url(self) -> str:
        return f"{settings.MEDIA_URL}{self.path}"
