# Generated by Django 3.0.7 on 2021-04-07 14:33

import base.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0010_auto_20210228_1831"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("description", models.CharField(default="bug fix", max_length=20)),
                ("text", models.TextField(default="")),
            ],
        ),
        migrations.AlterModelOptions(
            name="overview",
            options={"ordering": ("-created",)},
        ),
        migrations.RemoveField(
            model_name="outline",
            name="initial_outline_ruining_order",
        ),
        migrations.RemoveField(
            model_name="overview",
            name="targets",
        ),
        migrations.AddField(
            model_name="outline",
            name="initial_outline_buildings",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("headquarters", "Headquarters"),
                        ("barracks", "Barracks"),
                        ("stable", "Stable"),
                        ("workshop", "Workshop"),
                        ("academy", "Academy"),
                        ("smithy", "Smithy"),
                        ("rally_point", "Rally point"),
                        ("statue", "Statue"),
                        ("market", "Market"),
                        ("timber_camp", "Timber camp"),
                        ("clay_pit", "Clay pit"),
                        ("iron_mine", "Iron mine"),
                        ("farm", "Farm"),
                        ("warehouse", "Warehouse"),
                        ("wall", "wall"),
                    ],
                    max_length=100,
                ),
                default=base.models.building_default_list,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="messages",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="outline",
            name="avaiable_nobles",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, default=list, size=None
            ),
        ),
        migrations.AlterField(
            model_name="outline",
            name="avaiable_nobles_near",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, default=list, size=None
            ),
        ),
        migrations.AlterField(
            model_name="outline",
            name="avaiable_offs",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, default=list, size=None
            ),
        ),
        migrations.AlterField(
            model_name="outline",
            name="avaiable_offs_near",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, default=list, size=None
            ),
        ),
        migrations.AlterField(
            model_name="outline",
            name="initial_outline_catapult_default",
            field=models.IntegerField(
                choices=[(50, 50), (75, 75), (100, 100), (150, 150), (200, 200)],
                default=150,
            ),
        ),
        migrations.AlterField(
            model_name="outline",
            name="initial_outline_excluded_coords",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="weightmodel",
            name="building",
            field=models.CharField(
                blank=True,
                choices=[
                    ("headquarters", "Headquarters"),
                    ("barracks", "Barracks"),
                    ("stable", "Stable"),
                    ("workshop", "Workshop"),
                    ("academy", "Academy"),
                    ("smithy", "Smithy"),
                    ("rally_point", "Rally point"),
                    ("statue", "Statue"),
                    ("market", "Market"),
                    ("timber_camp", "Timber camp"),
                    ("clay_pit", "Clay pit"),
                    ("iron_mine", "Iron mine"),
                    ("farm", "Farm"),
                    ("warehouse", "Warehouse"),
                    ("wall", "wall"),
                ],
                default=None,
                max_length=50,
                null=True,
            ),
        ),
    ]
