# Generated by Django 5.0.1 on 2024-01-08 21:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0081_alter_outline_initial_outline_minimum_noble_troops"),
    ]

    operations = [
        migrations.AddField(
            model_name="outline",
            name="deff_collection_text_enroute",
            field=models.CharField(blank=True, default="", max_length=256),
        ),
        migrations.AddField(
            model_name="outline",
            name="deff_collection_text_in_village",
            field=models.CharField(blank=True, default="", max_length=256),
        ),
    ]