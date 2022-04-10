import os

from django.db import models
from django.conf import settings


class PDFPaymentSummary(models.Model):
    period = models.CharField(max_length=7, primary_key=True)
    path = models.CharField(max_length=300)

    def delete(self) -> tuple[int, dict[str, int]]:
        try:
            os.remove(f"{settings.MEDIA_ROOT}/{self.path}")
        except FileNotFoundError:
            pass

        return super().delete()

    def url(self) -> str:
        return f"{settings.MEDIA_URL}{self.path}"
