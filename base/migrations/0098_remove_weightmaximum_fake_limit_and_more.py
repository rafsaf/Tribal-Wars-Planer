# Generated by Django 5.1.8 on 2025-04-13 10:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0097_outline_initial_outline_minimum_fake_noble_troops"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="weightmaximum",
            name="fake_limit",
        ),
        migrations.RemoveField(
            model_name="weightmaximum",
            name="nobles_limit",
        ),
        migrations.AlterField(
            model_name="outline",
            name="initial_outline_nobles_limit",
            field=models.IntegerField(
                default=8,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(250),
                ],
            ),
        ),
    ]
