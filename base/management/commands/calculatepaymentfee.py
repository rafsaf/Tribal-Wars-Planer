# Copyright 2022 Rafał Safin (rafsaf). All Rights Reserved.
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
from time import sleep

import stripe
from django.conf import settings
from django.core.management.base import BaseCommand

import metrics
from base.management.commands.utils import job_logs_and_metrics
from base.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

log = logging.getLogger(__name__)


class Command(BaseCommand):  # pragma: no cover
    help = "Update stripe payments fees"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        processed = 0
        payment_without_new_date = Payment.objects.filter(new_date=None)
        for payment in payment_without_new_date:
            metrics.ERRORS.labels("payment_without_new_date found").inc()
            payment.save()  # signal handle_payment will be executed
            processed += 1
            sleep(0.5)

        payments_to_process = Payment.objects.filter(promotion=False, amount_pln=0)
        for payment in payments_to_process:
            if payment.from_stripe:
                if not payment.payment_intent_id:
                    event = stripe.Event.retrieve(id=payment.event_id)
                    sleep(0.2)

                    intent_id: str = event["data"]["object"]["payment_intent"]
                else:
                    intent_id = payment.payment_intent_id

                intent = stripe.PaymentIntent.retrieve(
                    intent_id, expand=["latest_charge"]
                )
                sleep(0.2)

                if "latest_charge" not in intent:
                    log.error(f"not exactly one charge in payment intent, {intent_id}")
                    metrics.ERRORS.labels("job:calculate_payment_fees").inc()
                    continue

                balance_transaction_id = intent["latest_charge"]["balance_transaction"]
                balance_transaction = stripe.BalanceTransaction.retrieve(
                    balance_transaction_id
                )
                sleep(0.2)

                if not balance_transaction["currency"].lower() == "pln":
                    log.error(
                        f"balance_transaction must be in pln, {balance_transaction_id}, intent: {intent_id}"
                    )
                    metrics.ERRORS.labels("job:calculate_payment_fees").inc()
                    continue

                payment.exchange_rate = balance_transaction["exchange_rate"]
                payment.payment_intent_id = intent_id
                payment.amount_pln = balance_transaction["amount"] / 100
                payment.fee_pln = balance_transaction["fee"] / 100
                payment.save()
            else:
                payment.amount_pln = payment.amount
                payment.fee_pln = 0
                payment.save()
            processed += 1
        log.info(f"updated {processed} payments")
