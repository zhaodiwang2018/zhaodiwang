# -*- coding: utf-8 -*-
# @Time    : 2019/10/15 18:11
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : clock.py
# @Software: PyCharm
from rest_framework.views import APIView, Response
from apps.land.serializers import *
from apps.land.forms import *
from apps.user.models import *
from apps.index.models import *
from rest_framework import serializers
from apps.utils.mixin_utils import *
import datetime
import time

from datetime import timezone
import pytz


class ClockRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClockRecord
        fields = ('create_on', 'question')


# TODO：打卡 get（用户今日是否已打卡） post（打卡，并提交一个问题）put（用户个人打卡记录）
class ClockView(LoginRequiredMixin, APIView):

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        today = datetime.date.today()
        today_str = time.mktime(today.timetuple())
        clock_a = ClockRecord.objects.filter(user_id=user.id).last()
        if not clock_a:
            return Response({'status': '1', 'is_clock': True})
        t = datetime.datetime(clock_a.create_on.year, clock_a.create_on.month, clock_a.create_on.day, 0, 0, 0)
        time_array = time.mktime(t.timetuple())
        if time_array == today_str:
            return Response({'status': '1', 'is_clock': False})
        else:
            return Response({'status': '1', 'is_clock': True})


    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        question = request.data.get('question')
        today = datetime.date.today()
        today_str = time.mktime(today.timetuple())
        clock_a = ClockRecord.objects.filter(user_id=user.id).last()
        if clock_a:
            t = datetime.datetime(clock_a.create_on.year, clock_a.create_on.month, clock_a.create_on.day, 0, 0, 0)
            time_array = time.mktime(t.timetuple())
            if time_array != today_str:
                ClockRecord.objects.create(user_id=user.id, question=question)
        else:
            ClockRecord.objects.create(user_id=user.id, question=question)
        user.integration += 58
        user.t_int += 58
        user.save()
        IntegralRecord.objects.create(integral_type='打卡挑刺积分', integral=58, user_id=user.id)

        return Response({'msg': '打卡成功', 'status': '1'})

    def put(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        clock_a = ClockRecord.objects.filter(user_id=user.id)
        seria = ClockRecordSerializers(clock_a, many=True)
        return Response({'msg': '成功', 'status': '1', 'data': seria.data})