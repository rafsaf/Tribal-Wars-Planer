# Generated by Django 4.0.3 on 2022-04-06 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0044_alter_stripeprice_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="stripeprice",
            options={"ordering": ["-active", "currency", "amount"]},
        ),
        migrations.AlterModelOptions(
            name="stripeproduct",
            options={"ordering": ["-active", "months"]},
        ),
    ]