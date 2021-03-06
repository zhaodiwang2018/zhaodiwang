# Generated by Django 2.1 on 2019-08-06 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190806_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='img',
            field=models.CharField(default='', max_length=32, verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='users',
            name='address_scale',
            field=models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='用地规模'),
        ),
        migrations.AlterField(
            model_name='users',
            name='area',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='区域'),
        ),
        migrations.AlterField(
            model_name='users',
            name='invest_pattern',
            field=models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='投资模式'),
        ),
        migrations.AlterField(
            model_name='users',
            name='land_nature',
            field=models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='用地性质'),
        ),
        migrations.AlterField(
            model_name='users',
            name='plot_ratio',
            field=models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='容积率'),
        ),
        migrations.AlterField(
            model_name='users',
            name='status',
            field=models.IntegerField(default=1, verbose_name='用户状态'),
        ),
    ]
