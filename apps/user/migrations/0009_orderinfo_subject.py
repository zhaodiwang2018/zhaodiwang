# Generated by Django 2.1 on 2019-08-14 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_orderinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='subject',
            field=models.CharField(default='', max_length=100, verbose_name='标题'),
        ),
    ]
