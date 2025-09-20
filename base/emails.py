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

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import activate

from base.models import Payment


def send_payment_email(payment: Payment, user: User) -> None:
    activate(payment.language)
    title = render_to_string(
        "email_payment_title.html",
        {"instance": payment},
    )
    msg_html = render_to_string(
        "email_payment_body.html",
        {
            "instance": payment,
            "domain": settings.MAIN_DOMAIN,
        },
    )
    send_mail(
        title,
        "",
        from_email=None,
        recipient_list=[user.email],
        html_message=msg_html,
    )
