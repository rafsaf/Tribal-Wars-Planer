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

stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = "Fetch and update stripe products and prices"

    def handle(self, *args, **options):
        # print(stripe.Product.list())
        print(stripe.Price.list())

        self.stdout.write(self.style.SUCCESS("Success"))
