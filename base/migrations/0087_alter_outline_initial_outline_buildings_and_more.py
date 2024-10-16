# Copyright 2024 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Generated by Django 5.1.1 on 2024-09-10 11:28

import django.contrib.postgres.fields
from django.db import migrations, models

import base.models.outline


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0086_alter_periodmodel_status"),
    ]

    operations = [
        migrations.AlterField(
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
                        ("wall", "Wall"),
                        ("watchtower", "Watchtower"),
                    ],
                    max_length=100,
                ),
                default=base.models.outline.building_default_list,
                size=None,
            ),
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
                    ("wall", "Wall"),
                    ("watchtower", "Watchtower"),
                ],
                default=None,
                max_length=50,
                null=True,
            ),
        ),
    ]
