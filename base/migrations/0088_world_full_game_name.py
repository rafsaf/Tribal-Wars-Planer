# Generated by Django 5.1.1 on 2024-09-10 12:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0087_alter_outline_initial_outline_buildings_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="world",
            name="full_game_name",
            field=models.CharField(default="", max_length=256),
        ),
    ]