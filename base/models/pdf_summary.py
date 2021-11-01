from typing import Any, Dict, Tuple
from django.db import models
from django.core.files.storage import FileSystemStorage
import os


class PDFPaymentSummary(models.Model):
    period = models.CharField(max_length=7, primary_key=True)
    path = models.CharField(max_length=300)

    def delete(self) -> Tuple[int, Dict[str, int]]:
        try:
            os.remove(f"media/{self.path}")
        except:
            pass
        return super().delete()

    def url(self) -> str:
        return f"/media/{self.path}"
