from django.db.models.query import QuerySet
from fpdf import FPDF
from base.models import PDFPaymentSummary, Payment
import os
from django.db.models import Max, Min

from datetime import date, datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import pytz
import secrets


class PDFPaymentsSummary(FPDF):
    def __init__(self, title: str, orientation="P", unit="mm", format="A4"):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.own_title = title

    def header(self):
        # Arial bold 15
        self.set_font("Arial", "B", 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(50, 10, self.own_title, 1, 0, "C")
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
    start_month = datetime(2021, 1, 1).replace(tzinfo=pytz.UTC)
    delta = relativedelta(months=1)
    now = timezone.now()
    for summary in PDFPaymentSummary.objects.all():
        summary.delete()
    while start_month < now:
        payments: QuerySet["Payment"] = Payment.objects.filter(
            status="finished",
            payment_date__year=start_month.year,
            payment_date__month=start_month.month,
        ).select_related("user")
        pdf = PDFPaymentsSummary(f"Summary {start_month.year}-{start_month.month}")
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
                f"{brutto} PLN : {netto} PLN : {payment.user.username} : {payment.payment_date} : {payment.event_id}",
                0,
                5,
            )
        if not os.path.exists("media"):
            os.makedirs("media")

        pdf.cell(0, 10, "", 0, 5)
        pdf.cell(0, 10, f"TOTAL BRUTTO: {total_brutto} PLN", 0, 5)
        pdf.cell(0, 10, f"TOTAL NETTO: {total_netto} PLN", 0, 5)
        pdf.cell(0, 10, f"GENERATED AT: {now}", 0, 5)
        pdf.cell(0, 10, f"PLEMIONA-PLANER.PL", 0, 5)

        name = str(start_month)[:7] + "-" + secrets.token_urlsafe() + ".pdf"

        pdf.output(f"media/{name}", "F")

        summary = PDFPaymentSummary.objects.create(
            path=name, period=f"{start_month.year}-{start_month.month}"
        )
        start_month = start_month + delta
