from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy


class Payment(models.Model):
    """Represents real payment, only superuser access"""

    STATUS = [
        ("finished", gettext_lazy("Finished")),
        ("returned", gettext_lazy("Returned")),
    ]
    status = models.CharField(max_length=30, choices=STATUS, default="finished")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    send_mail = models.BooleanField(default=True)
    amount = models.FloatField()
    event_id = models.CharField(max_length=300, null=True, default=None, blank=True)
    from_stripe = models.BooleanField(default=False)
    payment_date = models.DateField()
    months = models.IntegerField(default=1)
    comment = models.CharField(max_length=150, default="", blank=True)
    new_date = models.DateField(default=None, null=True, blank=True)

    def value(self) -> str:
        return f"{self.amount} PLN"
