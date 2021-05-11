""" Cronjobs """
from datetime import timedelta

from django.utils.timezone import now

from utils.database_update import cron_schedule_data_update
from . import models


def db_update():
    """Database update"""
    cron_schedule_data_update()


def outdate_overviews_delete():
    """Delete expired links"""
    expiration_data = now() - timedelta(days=30)
    expired = models.Overview.objects.filter(created__lt=expiration_data)
    expired.delete()
