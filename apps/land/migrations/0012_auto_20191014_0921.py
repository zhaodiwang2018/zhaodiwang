# Generated by Django 2.1 on 2019-10-14 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0011_auto_20191012_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landinfo',
            name='desc',
            field=models.CharField(blank=True, default='', max_length=400, null=True, verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='land_area',
            field=models.FloatField(blank=True, null=True, verbose_name='用地面积'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='start_price',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='起始价'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='title',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='标题'),
        ),
    ]
