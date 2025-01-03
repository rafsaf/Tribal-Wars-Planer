# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import datetime
import logging

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

import metrics
from base.emails import send_payment_email
from base.models import Message, Payment, Profile, Server
from utils.basic import create_test_world

log = logging.getLogger(__name__)


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
    if instance.new_date is not None:
        log.info("payment instance %s already is completed", instance)
    else:
        with transaction.atomic():
            instance = Payment.objects.select_for_update().get(pk=instance.pk)
            if instance.new_date is not None:
                log.info("payment instance %s already is completed", instance)
                return

            user = instance.user
            if user is None:
                log.critical("payment user is none, cannot proceed: %s", instance)
                metrics.ERRORS.labels("handle_payment").inc()
                return

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
                try:
                    send_payment_email(payment=instance, user=user)
                except Exception as e:
                    log.critical("unexpected error in send_payment_email: %s", e)
                    metrics.ERRORS.labels("handle_payment").inc()
                else:
                    instance.mail_sent = True

            instance.new_date = user_profile.validity_date
            user_profile.save()
            instance.save()
