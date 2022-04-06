# Generated by Django 4.0.2 on 2022-04-05 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0040_profile_currency"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="stripeprice",
            constraint=models.UniqueConstraint(
                fields=("amount", "currency"), name="unique price"
            ),
        ),
    ]
