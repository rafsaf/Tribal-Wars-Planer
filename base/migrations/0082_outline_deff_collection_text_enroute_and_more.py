# Copyright 2023 Rafał Safin (rafsaf). All Rights Reserved.
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
