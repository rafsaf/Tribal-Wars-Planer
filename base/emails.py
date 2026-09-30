# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

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
