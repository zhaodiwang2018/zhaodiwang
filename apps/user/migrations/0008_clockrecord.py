# Generated by Django 2.1 on 2019-10-15 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20191015_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClockRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0, verbose_name='id')),
                ('create_on', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('question', models.CharField(default='', max_length=500, verbose_name='问题')),
            ],
        ),
    ]
