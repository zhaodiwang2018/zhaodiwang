# Generated by Django 2.1 on 2019-08-21 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_auto_20190820_1831'),
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
    ]
