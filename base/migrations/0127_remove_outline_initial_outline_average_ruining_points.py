# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0126_remove_outline_initial_outline_catapult_max_value"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="outline",
            name="initial_outline_average_ruining_points",
        ),
    ]
