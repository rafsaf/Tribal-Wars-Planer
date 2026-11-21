import django.utils.timezone
from django.db import migrations, models
from django.db.models import OuterRef, Subquery
from django.db.models.functions import Coalesce


def fill_player_created_at(apps, schema_editor):
    Outline = apps.get_model("base", "Outline")
    Player = apps.get_model("base", "Player")
    WeightMaximum = apps.get_model("base", "WeightMaximum")
    outline_world = Outline.objects.filter(pk=OuterRef("outline_id"))
    WeightMaximum.objects.update(
        player_created_at=Coalesce(
            Subquery(
                Player.objects.filter(
                    world_id=Subquery(
                        Outline.objects.filter(
                            pk=OuterRef(OuterRef("outline_id"))
                        ).values("world_id")[:1]
                    ),
                    player_id=OuterRef("player_id"),
                ).values("created_at")[:1]
            ),
            Subquery(outline_world.values("world__created_at")[:1]),
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
