# Generated by Django 3.1.2 on 2020-11-16 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201115_1852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='startingBid',
            new_name='price',
        ),
    ]
