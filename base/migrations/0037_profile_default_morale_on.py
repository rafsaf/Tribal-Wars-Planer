# Generated by Django 4.0.2 on 2022-02-27 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0036_world_morale"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="default_morale_on",
            field=models.BooleanField(default=False),
        ),
    ]