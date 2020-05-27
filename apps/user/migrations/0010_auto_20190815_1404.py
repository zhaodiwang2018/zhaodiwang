# Generated by Django 2.1 on 2019-08-15 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_orderinfo_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='land_id',
            field=models.IntegerField(default=0, verbose_name='信息id'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='luyou',
            field=models.CharField(default='', max_length=32, verbose_name='路由'),
        ),
    ]
