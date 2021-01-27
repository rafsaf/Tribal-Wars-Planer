""" Cronjobs """
from datetime import timedelta

from django.utils.timezone import now

from tribal_wars.database_update import cron_schedule_data_update
from . import models

def db_update():
    """ Database update """
    cron_schedule_data_update()

def outdate_overviews_delete():
    """ Delete expired links """
    expiration_data = now() - timedelta(days=21)
    to_delete_lst = set()
    expired = models.Overview.objects.select_related().filter(created__lt=expiration_data)
    for overview in expired:
        to_delete_lst.add(overview.outline_overview.pk)
    
    models.OutlineOverview.objects.filter(pk__in=to_delete_lst).delete()
    expired.delete()
    
