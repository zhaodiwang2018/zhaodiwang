# Generated by Django 2.1 on 2019-10-14 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0012_auto_20191014_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landinfo',
            name='content',
            field=models.TextField(blank=True, default='', null=True, verbose_name='详细内容'),
        ),
    ]
