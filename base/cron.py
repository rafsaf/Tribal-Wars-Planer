""" Cronjobs """
from datetime import timedelta
from time import sleep

from django.utils.timezone import now
from django.db.models.query import QuerySet
from utils.database_update import cron_schedule_data_update

from . import models


def db_update():
    """Database update"""
    cron_schedule_data_update()


def outdate_overviews_delete():
    """Delete expired links"""
    expiration_date = now() - timedelta(days=30)
    expired = models.Overview.objects.filter(created__lt=expiration_date)
    expired.delete()


def outdate_outline_delete(days: int = 35) -> None:
    """Delete outlines older than 35 days except test World"""
    expiration_date = now() - timedelta(days=days)
    expired: "QuerySet[models.Outline]" = (
        models.Outline.objects.select_related("world")
        .filter(created__lt=expiration_date)
        .exclude(world__postfix="Test")
    )
    outline: models.Outline
    for outline in expired:
        outline.delete()
        sleep(0.2)
