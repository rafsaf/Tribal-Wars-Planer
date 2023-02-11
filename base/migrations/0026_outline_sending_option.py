# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
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

# Generated by Django 3.2.5 on 2021-08-09 21:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0025_outline_filter_weights_catapults_min"),
    ]

    operations = [
        migrations.AddField(
            model_name="outline",
            name="sending_option",
            field=models.CharField(
                choices=[
                    ("default", "Auto generated, fully equipped safe links"),
                    ("string", "Text simple in message"),
                    ("extended", "Text extended in message"),
                    ("table", "Table in message"),
                    ("deputy", "Text for deputy in message"),
                ],
                default="default",
                max_length=50,
            ),
        ),
    ]
