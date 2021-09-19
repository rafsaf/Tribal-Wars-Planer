from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from base.models import Message, Profile, Server
from utils.basic import create_test_world


@receiver(post_save, sender=Message)
def created_message(sender, instance, created, **kwargs):
    if created:
        Profile.objects.all().update(messages=F("messages") + 1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        default_server = Server.objects.get_or_create(dns="plemiona.pl", prefix="pl")[0]
        Profile.objects.create(user=instance, server=default_server)
    else:
        instance.profile.save()


@receiver(post_save, sender=Server)
def new_server_create_test_world(sender, instance, created, **kwargs):
    if created:
        create_test_world(server=instance)
