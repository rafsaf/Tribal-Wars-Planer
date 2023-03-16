from django.db import models


class OutlineWriteLock(models.Model):
    outline_id = models.BigIntegerField(primary_key=True)
    lock_expire = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
