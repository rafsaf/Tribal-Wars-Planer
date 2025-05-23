# Generated by Django 5.2 on 2025-05-06 16:27

from django.db import migrations, models


def feature_flag_shipments(apps, schema_editor) -> None:
    Profile = apps.get_model("base", "Profile")
    Profile.objects.update(feature_flag_shipments=True)


def reverse_feature_flag_shipments(apps, schema_editor) -> None:
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0106_profile_feature_flag_shipments"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="feature_flag_shipments",
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(
            code=feature_flag_shipments,
            reverse_code=reverse_feature_flag_shipments,
        ),
    ]
