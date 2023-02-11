# Generated by Django 4.0.4 on 2022-04-25 22:01

from django.db import migrations, models


def delete_all_pdfs(apps, schema_editor):
    PDFPaymentSummary = apps.get_model("base", "PDFPaymentSummary")
    for pdf in PDFPaymentSummary.objects.all():
        pdf.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0049_pdfpaymentsummary_created_at_and_more"),
    ]

    operations = [
        migrations.RunPython(delete_all_pdfs),
        migrations.AlterField(
            model_name="pdfpaymentsummary",
            name="period",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="pdfpaymentsummary",
            name="path",
            field=models.CharField(max_length=300, primary_key=True, serialize=False),
        ),
    ]
