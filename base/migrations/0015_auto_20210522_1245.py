# Generated by Django 3.2.2 on 2021-05-22 10:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20210521_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='outline',
            name='initial_outline_maximum_front_dist',
            field=models.IntegerField(default=120, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(400)]),
        ),
        migrations.AlterField(
            model_name='outline',
            name='initial_outline_front_dist',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)]),
        ),
    ]