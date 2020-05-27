# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 11:33
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : deleteoeder.py
# @Software: PyCharm
from rest_framework.views import APIView, Response
from apps.user.models import *
import datetime
import pytz


# 删除一天前的paying
class DeleteOrderPaying(APIView):
    def post(self, request):

        OneDayAgo = (datetime.datetime.now() - datetime.timedelta(days=1))
        # datetime 转utc格式
        OneDayAgo = OneDayAgo.replace(tzinfo=pytz.timezone('UTC'))

        orders = OrderInfo.objects.filter(pay_status='paying')
        for order in orders:

            if order.pay_time < OneDayAgo:
                order.delete()
                order.save()
        return Response({'data': '成功', 'status': '1'})

