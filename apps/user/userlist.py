# -*- coding: utf-8 -*-
# @Time    : 2019/9/27 17:28
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : userlist.py
# @Software: PyCharm
from rest_framework.views import APIView, Response
from apps.user.models import *
from apps.utils.mixin_utils import *
from rest_framework import serializers
import math
import datetime



class UserListsSerializers(serializers.ModelSerializer):
    yq_num = serializers.SerializerMethodField()
    ranking_company = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ('id', 'create_on', 'username', 'ranking_company', 'job', 'mobile', 'yq_num', 'company', 'city', 'area', 'addr', 'usertype', 'intro', 'vip_num', 'login_num', 'status', 'integration')

    def get_yq_num(self, obj):
        return InviteRegister.objects.filter(invite_peo_id=obj.id, yq_type='邀请注册').count()

    def get_ranking_company(self, obj):
        if obj.ranking_company:
            return obj.ranking_company
        return '无'

class UserListView(APIView):

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        if user.is_admin != 1:
            return Response({'msg': '非管理者，慎入！！', 'status': '0'})
        page = int(request.GET.get('page'))
        create_on = request.GET.get('create_on')
        usertype = request.GET.get('usertype')
        mobile = request.GET.get('mobile')
        # print(page, mobile)
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        if mobile:
            condition['mobile'] = mobile
        if usertype:
            condition['usertype'] = usertype
        condition['is_admin'] = 0
        users = Users.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = Users.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = UserListsSerializers(users, many=True)
        user_t = Users.objects.filter(is_admin=0, usertype='1').count()
        user_z = Users.objects.filter(is_admin=0, usertype='2').count()
        user_d = Users.objects.filter(is_admin=0, usertype='3').count()
        user_p = Users.objects.filter(is_admin=0, usertype='4').count()
        user_j = Users.objects.filter(is_admin=0, usertype='5').count()
        data_head = {'user_t': user_t,'user_z': user_z,'user_d': user_d,'user_p': user_p,'user_j': user_j,}
        return Response({'data': seria.data, 'data_head': data_head, 'total_page':total_page, 'msg': '获取用户列表成功', 'status': '1'})

    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        if user.is_admin != 1:
            return Response({'msg': '非管理者，慎入！！', 'status': '0'})
        status_user_id = request.data.get('status_user_id')
        status_user = Users.objects.filter(id=status_user_id).first()
        if status_user.status == 0:
            status_user.status = 1
        else:
            status_user.status = 0

        status_user.save()
        return Response({'msg': '冻结成功', 'status': '1'})


    def put(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        if user.is_admin != 1:
            return Response({'msg': '非管理者，慎入！！', 'status': '0'})
        company_user_id = request.data.get('company_user_id')
        company_user = request.data.get('company_user')
        print(company_user, company_user_id)
        c_user = Users.objects.filter(id=company_user_id).first()
        c_user.ranking_company = company_user
        c_user.save()
        if company_user:
            if c_user.usertype == '1':
                com = Company.objects.filter(username=company_user).first()
                if com:
                    com.register_num += 1
                else:
                    Company.objects.create(username=company_user, register_num=1)
        return Response({'msg': '修改成功', 'status': '1'})


class DataStatisticsSerializers(serializers.ModelSerializer):

    class Meta:
        model = AdminUserChart
        fields = ('user_all', 'new_user', 'today_chakan', 'today_shoucang', 'today_fufei', 'create_on')


class DataStatistics(APIView):

    def get(self, request):
        charts = AdminUserChart.objects.all().order_by('create_on')
        seria = DataStatisticsSerializers(charts, many=True)
        seven_days = datetime.timedelta(days=7)
        month_days = datetime.timedelta(days=30)
        today_time = datetime.date.today()
        weak_time = today_time - seven_days
        month_time = today_time - month_days
        today_info = AdminUserChart.objects.filter(create_on__gt=today_time)
        weak_info = AdminUserChart.objects.filter(create_on__gt=weak_time)
        month_info = AdminUserChart.objects.filter(create_on__gt=month_time)
        today_user = 0
        weak_user = 0
        month_user = 0
        for today in today_info:
            today_user += today.new_user
        for weak in weak_info:
            weak_user += weak.new_user
        for month in month_info:
            month_user += month.new_user
        return Response({'msg': '修改成功', 'status': '1', 'data': seria.data, 'today_user': today_user
                         , 'weak_user': weak_user, 'month_user': month_user})

    # def post(self,request):
        #