# Generated by Django 4.0.2 on 2022-02-21 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0035_outline_morale_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="world",
            name="morale",
            field=models.IntegerField(default=1),
        ),
    ]