# Generated by Django 2.1 on 2019-08-07 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0012_auto_20190807_0950'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ViewPeo',
            new_name='ReceivePeo',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='receiver_number',
        ),
        migrations.RemoveField(
            model_name='attractinfo',
            name='receiver_number',
        ),
        migrations.RemoveField(
            model_name='transinfo',
            name='receiver_number',
        ),
    ]
