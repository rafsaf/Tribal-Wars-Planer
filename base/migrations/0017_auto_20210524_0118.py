# Generated by Django 3.2.2 on 2021-05-23 23:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0016_weightmaximum_too_far_away"),
    ]

    operations = [
        migrations.AlterField(
            model_name="outline",
            name="initial_outline_front_dist",
            field=models.IntegerField(
                default=10,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(500),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="outline",
            name="initial_outline_maximum_front_dist",
            field=models.IntegerField(
                default=120,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1000),
                ],
            ),
        ),
    ]
