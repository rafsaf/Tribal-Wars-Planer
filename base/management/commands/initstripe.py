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


import stripe
from django.conf import settings
from base.models import StripeProduct
from django.core.management.base import BaseCommand
from django.db import transaction
from base.models.stripe_price import StripePrice

stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = "Fetch and update stripe products and prices"

    @transaction.atomic()
    def handle(self, *args, **options):
        StripeProduct.objects.all().delete()

        products = 0
        for item in stripe.Product.list():
            product = StripeProduct(
                product_id=item["id"],
                active=item["active"],
                created=item["created"],
                updated=item["updated"],
                name=item["name"],
                months=item["metadata"]["months"],
            )

            product.save()
            products += 1

        prices = 0
        for item in stripe.Price.list():
            if not item["type"] == "one_time":
                self.stdout.write(self.style.ERROR(f"Not one time price: {item['id']}"))
                continue
            price = StripePrice(
                price_id=item["id"],
                product_id=item["product"],
                active=item["active"],
                created=item["created"],
                currency=item["currency"].upper(),
                amount=item["unit_amount"],
            )
            price.save()
            prices += 1

        self.stdout.write(
            self.style.SUCCESS(f"Success, added {prices} prices & {products} products.")
        )
