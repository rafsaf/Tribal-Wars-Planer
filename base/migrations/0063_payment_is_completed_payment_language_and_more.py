# Generated by Django 4.1.3 on 2022-11-26 14:14

import secrets

from django.db import migrations, models

from base.models.payment import promotion_event_id


def payment_change_evt_id_to_unique(apps, schema_editor):
    Payment = apps.get_model("base", "Payment")
    for payment in Payment.objects.filter(event_id=None):
        if payment.promotion:
            payment.event_id = promotion_event_id()
            payment.save()
        else:
            payment.event_id = secrets.token_urlsafe(64)
            payment.save()


def reverse_pass(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0062_alter_profile_user"),
    ]

    operations = [
        migrations.RunPython(
            code=payment_change_evt_id_to_unique,
            reverse_code=reverse_pass,
        ),
        migrations.AddField(
            model_name="payment",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("pl", "Polish")],
                default="en",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="event_id",
            field=models.CharField(max_length=300, unique=True),
        ),
    ]