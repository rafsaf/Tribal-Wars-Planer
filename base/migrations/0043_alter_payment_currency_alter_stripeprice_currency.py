# Generated by Django 4.0.2 on 2022-04-05 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0042_payment_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="currency",
            field=models.CharField(
                choices=[("PLN", "PLN"), ("EUR", "EUR")], default="PLN", max_length=3
            ),
        ),
        migrations.AlterField(
            model_name="stripeprice",
            name="currency",
            field=models.CharField(
                choices=[("PLN", "PLN"), ("EUR", "EUR")], max_length=3
            ),
        ),
    ]