# Generated by Django 5.1.8 on 2025-04-13 19:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0103_remove_outline_initial_outline_ruin_full_offs_enabled"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="outline",
            name="initial_outline_off_left_catapult",
        ),
    ]
