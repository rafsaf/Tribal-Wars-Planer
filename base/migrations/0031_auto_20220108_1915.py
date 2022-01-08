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

# Generated by Django 3.2.11 on 2022-01-08 18:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0030_delete_documentation"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="server_bind",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="profile",
            name="server_bind_remind_not_before_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]