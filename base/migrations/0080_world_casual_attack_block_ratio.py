# Generated by Django 5.0 on 2024-01-02 13:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0079_alter_outline_sending_option_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="world",
            name="casual_attack_block_ratio",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]