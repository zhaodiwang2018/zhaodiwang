# Generated by Django 2.1 on 2019-11-05 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_users_ranking_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='ranking_company',
            field=models.CharField(default='无', max_length=50, verbose_name='公司排名'),
        ),
    ]
