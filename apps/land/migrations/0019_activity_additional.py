# Generated by Django 2.1 on 2019-08-22 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0018_auditopinion_yaoqing_yaoqingread'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='additional',
            field=models.CharField(default='', max_length=32, verbose_name='附加权益'),
        ),
    ]
