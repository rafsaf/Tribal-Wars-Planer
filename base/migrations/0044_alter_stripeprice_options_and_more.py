# Generated by Django 4.0.3 on 2022-04-06 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0043_alter_payment_currency_alter_stripeprice_currency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stripeprice',
            options={'ordering': ['-active']},
        ),
        migrations.AlterModelOptions(
            name='stripeproduct',
            options={'ordering': ['-active']},
        ),
    ]
