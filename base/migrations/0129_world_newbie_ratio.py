import django.utils.timezone
from django.db import migrations, models
from django.db.models import OuterRef, Subquery


def fill_player_created_at(apps, schema_editor):
    Outline = apps.get_model("base", "Outline")
    WeightMaximum = apps.get_model("base", "WeightMaximum")
    WeightMaximum.objects.update(
        player_created_at=Subquery(
            Outline.objects.filter(pk=OuterRef("outline_id")).values(
                "world__created_at"
            )[:1]
        )
    )


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0128_alter_outline_initial_outline_catapult_min_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="world",
            name="newbie_ratio",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="world",
            name="newbie_ratio_days",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="weightmaximum",
            name="player_created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RunPython(fill_player_created_at, migrations.RunPython.noop),
    ]
