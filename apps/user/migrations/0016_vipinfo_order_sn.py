# Generated by Django 2.1 on 2019-08-17 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20190817_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='vipinfo',
            name='order_sn',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='订单号'),
        ),
    ]
