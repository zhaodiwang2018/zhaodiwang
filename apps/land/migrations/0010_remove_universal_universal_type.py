# Generated by Django 2.1 on 2019-08-07 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0009_universal_universal_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='universal',
            name='universal_type',
        ),
    ]
