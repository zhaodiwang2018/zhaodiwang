# Generated by Django 2.1 on 2019-11-11 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUserChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_all', models.IntegerField(default=0, verbose_name='用户总数')),
                ('new_user', models.IntegerField(default=0, verbose_name='今日新增用户数')),
                ('today_chakan', models.IntegerField(default=0, verbose_name='今日查看数')),
                ('today_shoucang', models.IntegerField(default=0, verbose_name='今日收藏数')),
                ('today_fufei', models.IntegerField(default=0, verbose_name='今日付费数')),
                ('create_on', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
