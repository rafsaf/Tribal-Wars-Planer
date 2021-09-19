from django.db import models


class Server(models.Model):
    dns = models.CharField(max_length=50, primary_key=True)
    prefix = models.CharField(max_length=2)

    def __str__(self):
        return self.dns
