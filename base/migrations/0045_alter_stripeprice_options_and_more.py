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

# Generated by Django 4.0.3 on 2022-04-06 04:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0044_alter_stripeprice_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="stripeprice",
            options={"ordering": ["-active", "currency", "amount"]},
        ),
        migrations.AlterModelOptions(
            name="stripeproduct",
            options={"ordering": ["-active", "months"]},
        ),
    ]
