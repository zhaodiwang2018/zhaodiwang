# Generated by Django 2.1 on 2019-08-06 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190806_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='img',
            field=models.CharField(default='1565064301.png', max_length=32, verbose_name='头像'),
        ),
    ]
