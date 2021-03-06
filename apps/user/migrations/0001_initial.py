# Generated by Django 2.1 on 2019-09-05 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0, verbose_name='用户id')),
                ('nitui', models.IntegerField(default=0)),
                ('paimai', models.IntegerField(default=0)),
                ('zhuanrang', models.IntegerField(default=0)),
                ('zhaoshang', models.IntegerField(default=0)),
                ('xiancheng', models.IntegerField(default=0)),
                ('shalong', models.IntegerField(default=0)),
                ('yuebao', models.IntegerField(default=0)),
                ('nadi', models.IntegerField(default=0)),
                ('gongdi', models.IntegerField(default=0)),
                ('shoufang', models.IntegerField(default=0)),
                ('loupan', models.IntegerField(default=0)),
                ('yuebaodata', models.IntegerField(default=0)),
                ('zhoubao', models.IntegerField(default=0)),
                ('jibao', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_id', models.CharField(default='', max_length=64, verbose_name='id')),
                ('user_id', models.IntegerField(default=0, verbose_name='用户id')),
                ('luyou', models.CharField(default='', max_length=32, verbose_name='路由')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Contacted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_id', models.CharField(default='', max_length=64, verbose_name='id')),
                ('user_id', models.IntegerField(default=0, verbose_name='用户id')),
                ('luyou', models.CharField(default='', max_length=32, verbose_name='路由')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='LoginRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0, verbose_name='id')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='日期')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('luyou', models.CharField(default='', max_length=32, verbose_name='路由')),
                ('land_id', models.IntegerField(default=0, verbose_name='信息id')),
                ('order_sn', models.CharField(blank=True, max_length=50, null=True, verbose_name='订单号')),
                ('trade_no', models.CharField(blank=True, max_length=100, null=True, verbose_name='交易号')),
                ('pay_status', models.CharField(default='paying', max_length=30, verbose_name='订单状态')),
                ('subject', models.CharField(default='', max_length=100, verbose_name='标题')),
                ('order_mount', models.FloatField(default=0.0, verbose_name='订单金额')),
                ('pay_time', models.DateTimeField(auto_now_add=True, verbose_name='支付时间')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
            },
        ),
        migrations.CreateModel(
            name='ReleaseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0, verbose_name='发布用户id')),
                ('land_id', models.IntegerField(default=0, verbose_name='发布信息id')),
                ('luyou', models.CharField(default='', max_length=32, verbose_name='路由')),
                ('create_on', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='用户名')),
                ('mobile', models.CharField(max_length=50, verbose_name='手机号')),
                ('password', models.CharField(blank=True, max_length=5000, verbose_name='密码')),
                ('create_on', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('token', models.CharField(blank=True, max_length=300, null=True, verbose_name='头')),
                ('usertype', models.CharField(default='', max_length=16, verbose_name='用户类型')),
                ('status', models.IntegerField(default=1, verbose_name='用户状态')),
                ('city', models.CharField(blank=True, max_length=40, null=True, verbose_name='湖北省内主管城市')),
                ('job', models.CharField(blank=True, max_length=50, null=True, verbose_name='职位')),
                ('company', models.CharField(blank=True, max_length=50, null=True, verbose_name='公司名称')),
                ('addr', models.CharField(blank=True, max_length=50, null=True, verbose_name='公司地址')),
                ('address_scale', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='用地规模')),
                ('plot_ratio', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='容积率')),
                ('invest_pattern', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='投资模式')),
                ('land_nature', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='用地性质')),
                ('area', models.CharField(blank=True, max_length=40, null=True, verbose_name='区域')),
                ('intro', models.TextField(blank=True, null=True, verbose_name='个人简介')),
                ('img', models.CharField(default='1565251504.png', max_length=32, verbose_name='头像')),
                ('login_num', models.IntegerField(default=1, verbose_name='登陆次数')),
                ('is_admin', models.SmallIntegerField(default=0, verbose_name='是否管理者')),
                ('vip_num', models.IntegerField(default=0, verbose_name='vip')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='VipExpire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_time', models.DateTimeField(verbose_name='到期时间')),
                ('user_id', models.IntegerField(default=0, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Zan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('land_id', models.CharField(default='', max_length=64, verbose_name='id')),
                ('user_id', models.IntegerField(default=0, verbose_name='用户id')),
                ('luyou', models.CharField(default='', max_length=32, verbose_name='路由')),
                ('zc', models.IntegerField(default=0, verbose_name='赞或者踩')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='user.Users', verbose_name='用户'),
        ),
    ]
