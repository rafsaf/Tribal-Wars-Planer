# Generated by Django 5.0.6 on 2024-06-11 22:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0083_outlinewritelock_lock_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="outline",
            name="initial_outline_minimum_noble_troops",
            field=models.IntegerField(
                default=100,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(28000),
                ],
            ),
        ),
    ]