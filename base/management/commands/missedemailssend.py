# Copyright 2024 Rafał Safin (rafsaf). All Rights Reserved.
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


import logging

from django.core.management.base import BaseCommand
from django.db import transaction

import metrics
from base.emails import send_payment_email
from base.management.commands.utils import job_logs_and_metrics
from base.models.payment import Payment

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send unsend emails if they are not send already"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options) -> None:
        unsend_email_payments = Payment.objects.filter(
            send_mail=True,
            mail_sent=False,
            user__isnull=False,
        )

        for payment in unsend_email_payments:
            with transaction.atomic():
                instance = Payment.objects.select_for_update().get(pk=payment.pk)
                if instance.send_mail:
                    try:
                        assert instance.user, instance.pk
                        send_payment_email(payment=instance, user=instance.user)
                    except Exception as e:
                        log.critical("unexpected error in send_payment_email: %s", e)
                        metrics.ERRORS.labels("handle_payment").inc()
                    else:
                        instance.mail_sent = True

                instance.save()
