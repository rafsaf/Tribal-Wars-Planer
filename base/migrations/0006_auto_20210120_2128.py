# Generated by Django 3.0.7 on 2021-01-20 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_result_results_export"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="name",
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name="targetvertex",
            name="target",
            field=models.CharField(db_index=True, max_length=7),
        ),
        migrations.AlterField(
            model_name="tribe",
            name="tag",
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name="villagemodel",
            name="coord",
            field=models.CharField(db_index=True, max_length=7),
        ),
        migrations.AlterField(
            model_name="weightmaximum",
            name="start",
            field=models.CharField(db_index=True, max_length=7),
        ),
    ]
