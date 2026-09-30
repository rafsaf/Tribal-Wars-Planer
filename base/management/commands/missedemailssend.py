# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
                instance = (
                    Payment.objects.select_related("user")
                    .select_for_update(of=("self",))
                    .get(pk=payment.pk)
                )
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
