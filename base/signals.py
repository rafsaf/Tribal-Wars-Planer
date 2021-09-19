import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone

from base.models import Message, Payment, Profile, Server
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


@receiver(post_save, sender=Payment)
def handle_payment(sender, instance: Payment, created: bool, **kwargs) -> None:
    if created:
        user: User = instance.user
        user_profile: Profile = Profile.objects.get(user=user)

        current_date: datetime.date = timezone.localdate()
        relative_months: relativedelta = relativedelta(months=instance.months)
        day: relativedelta = relativedelta(days=1)
        if user_profile.validity_date is None:
            user_profile.validity_date = current_date + relative_months + day
        elif user_profile.validity_date <= current_date:
            user_profile.validity_date = current_date + relative_months + day
        else:
            user_profile.validity_date = (
                user_profile.validity_date + relative_months + day
            )

        if instance.send_mail:
            msg_html = render_to_string(
                "email_payment.html",
                {
                    "amount": instance.amount,
                    "payment_date": instance.payment_date,
                    "new_date": instance.new_date,
                    "user": instance.user,
                },
            )
            send_mail(
                "plemiona-planer.pl",
                "",
                "plemionaplaner.pl@gmail.com",
                recipient_list=[user.email],
                html_message=msg_html,
            )

        instance.new_date = user_profile.validity_date
        user_profile.save()
        instance.save()
