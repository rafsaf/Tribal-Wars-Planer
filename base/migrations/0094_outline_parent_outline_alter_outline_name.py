# Generated by Django 5.1.2 on 2024-12-15 17:42

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0093_server_tz"),
    ]

    operations = [
        migrations.AddField(
            model_name="outline",
            name="parent_outline",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="base.outline",
            ),
        ),
        migrations.AlterField(
            model_name="outline",
            name="name",
            field=models.CharField(
                max_length=32,
                validators=[
                    django.core.validators.MinLengthValidator(1),
                    django.core.validators.MaxLengthValidator(24),
                ],
            ),
        ),
    ]
