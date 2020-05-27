# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 9:43
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : rili.py
# @Software: PyCharm
from rest_framework.views import APIView, Response
from apps.user.models import *
from apps.land.models import *
from apps.utils.mixin_utils import *
from rest_framework import serializers
import time
import datetime


class RenMaiView(APIView):

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        fabu_info = ReleaseRecord.objects.filter(user_id=user.id, luyou='/tudimessage/zhuanrang')
        guanzhu = 0
        if fabu_info:
            for fabu in fabu_info:
                info_guanzhu = ReceivePeo.objects.filter(information_id=fabu.land_id, luyou='/tudimessage/zhuanrang').count()
                print(info_guanzhu)
                guanzhu += info_guanzhu
        return Response({'msg': '成功', 'status': '1', 'fabu': fabu_info.count(), 'guanzhu':guanzhu})

# 日历和备忘录的首页展示
class RiLiHomePageView(LoginRequiredMixin, APIView):

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        today = datetime.date.today()
        c_date = request.GET.get('c_date')
        c_list = Calendar.objects.filter(c_date=c_date).first()
        m_list = Memo.objects.filter(user_id=user.id, m_date=today).first()
        if c_list:
            rili_num = len(eval(c_list.big_list))
        else:
            rili_num = 0
        if m_list:
            b_num = len(eval(m_list.content))
        else:
            b_num = 0
        return Response({'msg': '成功', 'status': '1', 'rili_num': rili_num, 'b_num': b_num})



class CityListView(LoginRequiredMixin, APIView):
    def get(self, request):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        today_timeArray = time.strptime(str(yesterday)[:10], "%Y-%m-%d")
        # 今天的时间戳
        today_time = time.mktime(today_timeArray)
        city_list = []
        big_s = Calendar.objects.all()
        for big_ in big_s:
            timeArray = time.strptime(big_.c_date[:10], "%Y-%m-%d")

            timestamp = time.mktime(timeArray)
            if today_time <= timestamp:
                big_list = eval(str(big_.big_list))
                time_list = []
                for b_list in big_list:
                    for city, info_list in b_list.items():
                        land_guapai = 0
                        land_paimai = 0
                        for info in info_list:
                            # print(b)
                            if info['land_type'] == 1:
                                land_guapai += 1
                            else:
                                land_paimai += 1
                        c_dic = {'city': city, 'land_guapai': land_guapai, 'land_paimai': land_paimai}
                        time_list.append(c_dic)
                city_list.append({big_.c_date: time_list})
        return Response({'msg': '成功', 'status': '1', 'city_list': city_list})

    def post(self, request):
        r_day = request.data.get('r_day')
        city = request.data.get('city')
        info = Calendar.objects.filter(c_date=r_day).first()
        for big in eval(info.big_list):
            for c, i in big.items():
                if c == city:
                    return Response({'msg': '成功', 'status': '1', 'city_info': i})
        return Response({'msg': '成功', 'status': '1', 'city_list': info.big_list})


class MeMoViewSerializers(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    class Meta:
        model = Memo
        fields = ('m_date', 'content',)

    def get_content(self, obj):
        return eval(obj.content)


# TODO：备忘录
class MeMoView(LoginRequiredMixin, APIView):
    def get(self, request):
        m_date = request.GET.get('m_date')
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        user_date = Memo.objects.filter(user_id=user.id, m_date=m_date).first()
        if not user_date:
            return Response({'msg': '无备忘录', 'status': '2'})
        return Response({'msg': '成功', 'status': '1', 'data': user_date.content})

    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        content = request.data.get('content')
        m_date = request.data.get('m_date')
        user_m_date = Memo.objects.filter(user_id=user.id, m_date=m_date).first()
        if not content:
            user_m_date.delete()
            return Response({'msg': '成功', 'status': '1'})
        if not user_m_date:
            Memo.objects.create(user_id=user.id, m_date=m_date, content=content)
            return Response({'msg': '成功', 'status': '1'})
        user_m_date.content = content
        user_m_date.save()
        return Response({'msg': '成功', 'status': '1'})

    def put(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        memo_info = Memo.objects.filter(user_id=user.id)
        seria = MeMoViewSerializers(memo_info, many=True)
        return Response({'msg': '成功', 'status': '1', 'data': seria.data})


class MeMoListView(LoginRequiredMixin, APIView):

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        today = datetime.date.today()
        today_timeArray = time.strptime(str(today)[:10], "%Y-%m-%d")
        # 今天的时间戳
        today_time = time.mktime(today_timeArray)
        memo_user = Memo.objects.filter(user_id=user.id)
        memo_list = []
        for memo in memo_user:
            timeArray = time.strptime(memo.m_date, "%Y-%m-%d")
            # print(timeArray)
            timestamp = time.mktime(timeArray)
            if timestamp >= today_time:
                memo_list.append({'m_date': memo.m_date, 'content': memo.content})
        return Response({'msg': '成功', 'status': '1', 'data': memo_list})