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

import secrets
from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta
from django.db.models.query import QuerySet
from django.utils import timezone
from fpdf import FPDF

from base.models import Payment, PDFPaymentSummary


class PDFPaymentsSummary(FPDF):
    def __init__(self, title: str, orientation="P", unit="mm", format="A4"):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.own_title = title

    def header(self):
        # Arial bold 15
        self.set_font("Arial", "B", 15)
        # Move to the right
        self.cell(40)
        # Title
        self.cell(90, 10, self.own_title, 1, 0, "C")
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font("Arial", "I", 8)
        # Page number
        self.cell(0, 10, f"Page {str(self.page_no())}/" + "{nb}", 0, 0, "C")


def generate_pdf_summary():
    years_result: dict[int, dict[str, float]] = {}

    current_datetime = datetime(2021, 1, 1).replace(tzinfo=pytz.UTC)
    delta = relativedelta(months=1)
    now = timezone.now()
    for summary in PDFPaymentSummary.objects.all():
        summary.delete()
    while current_datetime < now:
        if current_datetime.year not in years_result:
            years_result[current_datetime.year] = {"brutto": 0, "netto": 0}

        payments: QuerySet[Payment] = Payment.objects.filter(
            status="finished",
            payment_date__year=current_datetime.year,
            payment_date__month=current_datetime.month,
        ).select_related("user")
        pdf = PDFPaymentsSummary(
            f"Summary {current_datetime.year}-{current_datetime.month}"
        )
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font("Times", "", 12)

        pdf.cell(
            0,
            10,
            "AMOUNT BRUTTO : AMOUNT NETTO : USERNAME : DATE : (STRIPE ID)",
            0,
            5,
        )
        exact_fees = {
            30: 1.57,
            55: 1.77,
            70: 1.98,
        }
        total_netto = 0
        total_brutto = 0
        for payment in payments:
            brutto: float = float(payment.amount)
            if payment.from_stripe:
                try:
                    netto = brutto - exact_fees[payment.amount]
                except KeyError:
                    netto = brutto - brutto * 1.4 - 1
            else:
                netto = brutto
            total_netto += netto
            total_brutto += brutto

            pdf.cell(
                0,
                10,
                (
                    f"{brutto} PLN : {netto} PLN : "
                    f"{str(payment.user.username).encode('latin-1', 'replace').decode('latin-1')} : "
                    f"{payment.payment_date} : {payment.event_id}"
                ),
                0,
                5,
            )
        years_result[current_datetime.year]["brutto"] += total_brutto
        years_result[current_datetime.year]["netto"] += total_netto

        pdf.cell(0, 10, "", 0, 5)
        pdf.cell(0, 10, f"TOTAL BRUTTO: {total_brutto} PLN", 0, 5)
        pdf.cell(0, 10, f"TOTAL NETTO: {total_netto} PLN", 0, 5)
        pdf.cell(0, 10, f"GENERATED AT: {now}", 0, 5)
        pdf.cell(0, 10, "PLEMIONA-PLANER.PL", 0, 5)

        name = str(current_datetime)[:7] + "-" + secrets.token_urlsafe(80) + ".pdf"

        pdf.output(f"media/{name}", "F")  # type: ignore

        summary = PDFPaymentSummary.objects.create(
            path=name, period=f"{current_datetime.year}-{current_datetime.month}"
        )
        current_datetime = current_datetime + delta

    for yearly_result in years_result:
        pdf = PDFPaymentsSummary(f"Summary for year {yearly_result}")
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font("Times", "", 12)
        pdf.cell(0, 10, "", 0, 5)
        pdf.cell(
            0, 10, f"TOTAL BRUTTO: {years_result[yearly_result]['brutto']} PLN", 0, 5
        )
        pdf.cell(
            0, 10, f"TOTAL NETTO: {years_result[yearly_result]['netto']} PLN", 0, 5
        )
        pdf.cell(0, 10, f"GENERATED AT: {now}", 0, 5)
        pdf.cell(0, 10, "PLEMIONA-PLANER.PL", 0, 5)
        name = str(current_datetime)[:7] + "-" + secrets.token_urlsafe(80) + ".pdf"
        pdf.output(f"media/{name}", "F")  # type: ignore
        summary = PDFPaymentSummary.objects.create(
            path=name, period=f"{yearly_result}all"
        )
