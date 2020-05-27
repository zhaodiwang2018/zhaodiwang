# Generated by Django 2.1 on 2019-10-12 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0008_auto_20191012_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landinfo',
            name='house_account',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='住房比'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='location',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='位置'),
        ),
    ]
