# Generated by Django 2.1 on 2019-10-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0010_auto_20191012_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landinfo',
            name='add_amplitude',
            field=models.CharField(blank=True, default='', max_length=32, null=True, verbose_name='加价幅度'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='advance_date',
            field=models.CharField(default='', max_length=50, verbose_name='预告日期'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='building_density',
            field=models.FloatField(blank=True, null=True, verbose_name='建筑密度'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='content',
            field=models.TextField(default='', verbose_name='详细内容'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='deal_remark',
            field=models.CharField(default='', max_length=64, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='deal_time',
            field=models.CharField(default='', max_length=32, verbose_name='成交时间'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='desc',
            field=models.CharField(default='', max_length=400, verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='greening',
            field=models.FloatField(blank=True, null=True, verbose_name='绿化率'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='house_account',
            field=models.CharField(default='', max_length=64, null=True, verbose_name='住房比'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='information_source',
            field=models.CharField(default='', max_length=200, verbose_name='信息来源'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='is_deal',
            field=models.IntegerField(default=0, verbose_name='是否成交'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='is_publish',
            field=models.IntegerField(default=0, verbose_name='是否已发布'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='land_area',
            field=models.FloatField(default=0, verbose_name='用地面积'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='land_nature',
            field=models.CharField(default='', max_length=100, verbose_name='用地性质'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='listed_date',
            field=models.CharField(default='', max_length=50, verbose_name='挂牌日期'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='location',
            field=models.CharField(default='', max_length=500, verbose_name='位置'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='margin',
            field=models.FloatField(default=0, verbose_name='保证金'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='now_progress',
            field=models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='目前进度'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='plot_ratio',
            field=models.FloatField(blank=True, null=True, verbose_name='容积率'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='reward_price',
            field=models.FloatField(default=0.01, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='serial_number',
            field=models.CharField(default='', max_length=200, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='special_requirements',
            field=models.CharField(blank=True, default='', max_length=256, null=True, verbose_name='特殊要求'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='start_price',
            field=models.FloatField(default=0, verbose_name='起始价'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='title',
            field=models.CharField(default='', max_length=100, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='transfer_date',
            field=models.CharField(default='', max_length=50, verbose_name='出让日期'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='transfer_mode',
            field=models.CharField(default='', max_length=200, verbose_name='出让方式'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='transferee_peo',
            field=models.CharField(default='', max_length=32, verbose_name='受让人'),
        ),
        migrations.AlterField(
            model_name='landinfo',
            name='yuji_guapai',
            field=models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='预计挂牌时间'),
        ),
        migrations.AlterField(
            model_name='transinfo',
            name='title',
            field=models.CharField(default='', max_length=100, verbose_name='标题'),
        ),
    ]
