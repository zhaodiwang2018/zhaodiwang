# Generated by Django 2.1 on 2019-08-20 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_cai_contact_contacted_zan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='支付时间'),
        ),
    ]
