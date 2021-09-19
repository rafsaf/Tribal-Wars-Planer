from django.db import models


class Message(models.Model):
    date = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=20, default="bug fix")
    text = models.TextField(default="")
