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

import stripe
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from base.management.commands.utils import job_logs_and_metrics
from base.models import StripePrice, StripeProduct

stripe.api_key = settings.STRIPE_SECRET_KEY

log = logging.getLogger(__name__)


@transaction.atomic()
def synchronize_stripe():  # pragma: no cover
    StripeProduct.objects.all().delete()
    log.info("Started synchonization of stripe")
    products = 0
    for product_item in stripe.Product.list():
        if "months" not in product_item["metadata"]:
            log.warning(
                f"No months in metadata, skipping product: {product_item['id']}"
            )
            continue
        product = StripeProduct(
            product_id=product_item["id"],
            active=product_item["active"],
            created=product_item["created"],
            updated=product_item["updated"],
            name=product_item["name"],
            months=product_item["metadata"]["months"],
        )

        product.save()
        products += 1

    prices = 0
    for price_item in stripe.Price.list():
        currency = price_item["currency"].upper()
        if not price_item["type"] == "one_time":
            log.warning(f"Not one time price: {price_item['id']}")
            continue
        if currency not in settings.SUPPORTED_CURRENCIES:
            log.warning(
                f"Currency {price_item['currency']} not supported: {price_item['id']}"
            )
            continue

        try:
            product = StripeProduct.objects.get(product_id=price_item["product"])
        except StripeProduct.DoesNotExist:
            log.warning(
                f"Product {price_item['product']} does not exists, skipping price: {price_item['id']}"
            )
            continue

        price = StripePrice(
            price_id=price_item["id"],
            product_id=price_item["product"],
            active=price_item["active"],
            created=price_item["created"],
            currency=currency,
            amount=price_item["unit_amount"],
        )
        price.save()
        prices += 1
    return prices, products


class Command(BaseCommand):  # pragma: no cover
    help = "Fetch and update stripe products and prices"

    @job_logs_and_metrics(log)
    def handle(self, *args, **options):
        if settings.STRIPE_SECRET_KEY:
            prices, products = synchronize_stripe()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Success, added {prices} prices & {products} products."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Skipping, no STRIPE_SECRET_KEY setting found.")
            )
