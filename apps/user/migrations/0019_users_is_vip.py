# Generated by Django 2.1 on 2019-08-17 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20190817_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_vip',
            field=models.IntegerField(default=0, verbose_name='是否vip'),
        ),
    ]
