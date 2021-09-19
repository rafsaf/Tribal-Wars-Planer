import datetime
from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

if TYPE_CHECKING:
    from base.models import Message


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    server = models.ForeignKey(
        "Server", on_delete=models.SET_NULL, null=True, default=None
    )
    validity_date = models.DateField(
        default=datetime.date(year=2021, month=2, day=25), blank=True, null=True
    )
    messages = models.IntegerField(default=0)

    def is_premium(self) -> bool:
        if self.validity_date is None:
            return False
        today = timezone.localdate()
        if today > self.validity_date:
            return False
        return True

    def latest_messages(self) -> "QuerySet[Message]":
        from base.models.message import Message

        return Message.objects.order_by("-created")[:6]
