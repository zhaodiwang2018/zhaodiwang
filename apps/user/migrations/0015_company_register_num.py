# Generated by Django 2.1 on 2019-11-02 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='register_num',
            field=models.FloatField(default=0.0, verbose_name='积分'),
        ),
    ]
