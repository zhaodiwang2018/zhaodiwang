# -*- coding: utf-8 -*-
# @Time    : 2019/8/29 9:12
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : delivery.py
# @Software: PyCharm

from rest_framework.views import APIView, Response
from apps.user.models import *
from apps.utils.mixin_utils import *
from rest_framework import serializers
from apps.land.models import *
from apps.user.models import Users
from apps.index.models import *

import datetime, pytz
import time
import random


# 拍卖
class DeliveryPaiMaiSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()
    building_area = serializers.SerializerMethodField()
    detail_info = serializers.SerializerMethodField()
    pay_time = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()

    class Meta:
        model = LandInfo
        fields = (
            'title', 'pay_time', 'luyou', 'serial_number', 'city', 'area', 'land_nature', 'transfer_mode', 'land_area',
            'start_price', 'sale_price',
            'location', 'plot_ratio', 'building_area', 'plan_condition', 'add_amplitude', 'advance_date',
            'listed_date', 'transfer_date', 'img', 'detail_info', 'remark', 'house_account', 'file_url',
            'img_list')

    def get_luyou(self, obj):
        return '拍卖公告'

    def get_building_area(self, obj):
        return round(obj.land_area * obj.plot_ratio, 2)

    def get_detail_info(self, obj):
        release = ReleaseRecord.objects.filter(land_id=obj.id, luyou='/tudimessage/paimai').first()
        user = Users.objects.filter(id=release.user_id).first()
        return user.username + user.mobile

    def get_pay_time(self, obj):
        order = OrderInfo.objects.filter(land_id=obj.id, luyou='/tudimessage/paimai',
                                         user_id=self.context['user_id']).first()
        if order:
            return order.pay_time
        return ''

    def get_sale_price(self, obj):
        return round(obj.start_price * 10000 / obj.land_area)


# 拟推
class DeliveryNiTuiSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()
    building_area = serializers.SerializerMethodField()
    detail_info = serializers.SerializerMethodField()
    pay_time = serializers.SerializerMethodField()

    class Meta:
        model = LandInfo
        fields = (
            'title', 'pay_time', 'luyou', 'serial_number', 'city', 'area', 'land_nature', 'transfer_mode', 'land_area',
            'yuji_guapai',
            'location', 'plot_ratio', 'building_area', 'plan_condition', 'now_progress', 'img', 'detail_info',
            'remark', 'house_account', 'file_url', 'img_list')

    def get_luyou(self, obj):
        return '拟推预告'

    def get_building_area(self, obj):
        return round(obj.land_area * obj.plot_ratio, 2)

    def get_detail_info(self, obj):
        release = ReleaseRecord.objects.filter(land_id=obj.id, luyou='/tudimessage/nitui').first()
        user = Users.objects.filter(id=release.user_id).first()
        return user.username + user.mobile

    def get_pay_time(self, obj):
        order = OrderInfo.objects.filter(land_id=obj.id, luyou='/tudimessage/nitui',
                                         user_id=self.context['user_id']).first()
        if order:
            return order.pay_time
        return ''


# 县城
class DeliveryXianChengSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()
    building_area = serializers.SerializerMethodField()
    detail_info = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    pay_time = serializers.SerializerMethodField()

    class Meta:
        model = LandInfo
        fields = (
            'title', 'pay_time', 'luyou', 'serial_number', 'city', 'area', 'land_nature', 'transfer_mode', 'land_area',
            'start_price',
            'location', 'plot_ratio', 'building_area', 'plan_condition', 'img', 'detail_info', 'advance_date',
            'listed_date', 'transfer_date', 'special_requirements', 'sale_price',
            'remark', 'house_account', 'file_url', 'img_list')

    def get_luyou(self, obj):
        return '县城土地'

    def get_building_area(self, obj):
        return round(obj.land_area * obj.plot_ratio, 2)

    def get_sale_price(self, obj):
        return round(obj.start_price * 10000 / (obj.land_area * obj.plot_ratio))

    def get_detail_info(self, obj):
        release = ReleaseRecord.objects.filter(land_id=obj.id, luyou='/tudimessage/xiancheng').first()
        user = Users.objects.filter(id=release.user_id).first()
        return user.username + user.mobile

    def get_pay_time(self, obj):
        order = OrderInfo.objects.filter(land_id=obj.id, luyou='/tudimessage/xiancheng',
                                         user_id=self.context['user_id']).first()
        if order:
            return order.pay_time
        return ''


# 转让
class DeliveryZhuanRangSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()
    building_area = serializers.SerializerMethodField()
    detail_info = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    pay_time = serializers.SerializerMethodField()

    class Meta:
        model = TransInfo
        fields = ('title', 'pay_time', 'luyou', 'serial_number', 'city', 'area', 'land_nature', 'land_area', 'price',
                  'information_validity', 'location', 'plot_ratio', 'building_area', 'plan_conditions', 'img',
                  'detail_info', 'trading_type', 'trading_conditions', 'sale_price', 'people', 'contact',
                  'remark', 'house_account', 'file_url', 'img_list')

    def get_luyou(self, obj):
        return '转让信息'

    def get_building_area(self, obj):
        return round(obj.land_area * obj.plot_ratio, 2)

    def get_sale_price(self, obj):
        return round(obj.price * 10000 / (obj.land_area * obj.plot_ratio))

    def get_detail_info(self, obj):
        return obj.people + obj.contact

    def get_pay_time(self, obj):
        order = OrderInfo.objects.filter(land_id=obj.id, luyou='/tudimessage/zhuanrang',
                                         user_id=self.context['user_id']).first()
        if order:
            return order.pay_time
        return ''


# 招商
class DeliveryZhaoShangSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()
    building_area = serializers.SerializerMethodField()
    detail_info = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    pay_time = serializers.SerializerMethodField()

    class Meta:
        model = AttractInfo
        fields = (
            'title', 'pay_time', 'luyou', 'serial_number', 'city', 'area', 'land_nature', 'total_inv', 'land_area',
            'industry_requirements', 'location', 'plot_ratio', 'building_area', 'img', 'detail_info', 'people',
            'contact', 'cooperate_condition', 'sale_price', 'remark', 'house_account', 'file_url', 'img_list')

    def get_luyou(self, obj):
        return '招商信息'

    def get_building_area(self, obj):
        return round(obj.land_area * obj.plot_ratio, 2)

    def get_sale_price(self, obj):
        return round(obj.total_inv * 10000 / (obj.land_area * obj.plot_ratio))

    def get_detail_info(self, obj):
        return obj.people + obj.contact

    def get_pay_time(self, obj):
        order = OrderInfo.objects.filter(land_id=obj.id, luyou='/tudimessage/zhaoshang',
                                         user_id=self.context['user_id']).first()
        if order:
            return order.pay_time
        return ''


# 活动
class DeliveryActivitySerializers(serializers.ModelSerializer):
    create_on = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'activity_datetime', 'activity_place', 'information_source',
            'reward_price', 'create_on', 'traffic_tips', 'content_feed')

    def get_create_on(self, obj):

        if obj.activity_type == '1':
            order = OrderInfo.objects.filter(luyou='/activity/shalong', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        elif obj.activity_type == '2':
            order = OrderInfo.objects.filter(luyou='/activity/yuebao', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        elif obj.activity_type == '3':
            order = OrderInfo.objects.filter(luyou='/activity/tuijie', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        else:
            order = OrderInfo.objects.filter(luyou='/activity/kuanian', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''


# 榜单
class DeliveryPopListSerializers(serializers.ModelSerializer):
    create_on = serializers.SerializerMethodField()

    class Meta:
        model = PropertyList
        fields = ('title', 'create_on', 'file_url', 'file_introduction')

    def get_create_on(self, obj):
        if obj.property_type == '1':
            order = OrderInfo.objects.filter(luyou='/tudilist/nadi', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        elif obj.property_type == '2':
            order = OrderInfo.objects.filter(luyou='/tudilist/gongdi', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        elif obj.property_type == '3':
            order = OrderInfo.objects.filter(luyou='/tudilist/shoulou', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        else:
            order = OrderInfo.objects.filter(luyou='/tudilist/loupan', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''


# 数据
class DeliveryInvSerializers(serializers.ModelSerializer):
    create_on = serializers.SerializerMethodField()

    class Meta:
        model = InvestmentData
        fields = ('title', 'create_on', 'file_url', 'file_introduction')

    def get_create_on(self, obj):
        if obj.property_type == '1':
            order = OrderInfo.objects.filter(luyou='/Investment/zhoubao', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        elif obj.property_type == '2':
            order = OrderInfo.objects.filter(luyou='/Investment/yuebao', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        elif obj.property_type == '3':
            order = OrderInfo.objects.filter(luyou='/Investment/jibao', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        elif obj.property_type == '4':
            order = OrderInfo.objects.filter(luyou='/Investment/bannianbao', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''
        else:
            order = OrderInfo.objects.filter(luyou='/Investment/nianbao', land_id=obj.id,
                                             user_id=self.context['user_id']).first()
            if order:
                return order.pay_time
            return ''


class DeliveryLandView(APIView):

    def get_is_vip(self, user_id):
        vip = VipExpire.objects.filter(user_id=user_id).first()
        if vip:
            if vip.expire_time.replace(tzinfo=pytz.timezone('UTC')) > datetime.datetime.now().replace(
                    tzinfo=pytz.timezone('UTC')):
                return True
            return False
        return False

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        land_id = request.GET.get('land_id')
        luyou = request.GET.get('luyou', '/activity/shalong')
        order = OrderInfo.objects.filter(user_id=user.id, land_id=land_id, luyou=luyou,
                                         pay_status='TRADE_SUCCESS').first()
        if order or self.get_is_vip(user.id) is True:
            z_c = Zan.objects.filter(user_id=user.id, land_id=land_id, luyou=luyou).first()
            if z_c:
                if z_c.zc == 1:
                    zc_data = {'zc_data': '赞'}
                elif z_c.zc == 2:
                    zc_data = {'zc_data': '踩'}
                else:
                    zc_data = {'zc_data': '无'}
            else:
                zc_data = {'zc_data': '无'}

            if luyou == '/tudimessage/paimai':
                land_info = LandInfo.objects.filter(id=land_id)
                seria = DeliveryPaiMaiSerializers(land_info, many=True, context={'user_id': user.id})
                return Response({'status': '1', 'msg': '成功', 'data': seria.data, 'zc_data': zc_data})
            elif luyou == '/tudimessage/nitui':
                land_info = LandInfo.objects.filter(id=land_id)
                seria = DeliveryNiTuiSerializers(land_info, many=True, context={'user_id': user.id})
                return Response({'status': '1', 'msg': '成功', 'data': seria.data, 'zc_data': zc_data})
            elif luyou == '/tudimessage/xiancheng':
                land_info = LandInfo.objects.filter(id=land_id)
                seria = DeliveryXianChengSerializers(land_info, many=True, context={'user_id': user.id})
                return Response({'status': '1', 'msg': '成功', 'data': seria.data, 'zc_data': zc_data})
            elif luyou == '/tudimessage/zhuanrang':
                if self.get_is_vip(user.id) is True:
                    trans = TransInfo.objects.filter(id=land_id).first()
                    order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                                   userid=user.id, ranstr=random.randint(10, 99))
                    a = time.time()
                    trade_no = str(int(a * 100000))
                    OrderInfo.objects.create(user_id=user.id, order_mount=trans.reward_price, order_sn=order_sn,
                                             subject=trans.title, trade_no=trade_no,
                                             land_id=land_id, luyou=luyou, pay_status='TRADE_SUCCESS', order_type=5)
                    # TODO:
                    fabu = ReleaseRecord.objects.filter(land_id=land_id, luyou=luyou).first()
                    if not Contact.objects.create(user_id=user.id, land_id=land_id,
                                                  contacted_id=fabu.user_id, luyou=luyou):
                        Contact.objects.create(user_id=user.id, land_id=land_id,
                                               contacted_id=fabu.user_id, luyou=luyou)

                    order_vip = OrderInfo.objects.filter(order_sn=order_sn).first()
                    contented = '恭喜您,您的' + order_vip.subject + '订单，已被会员' + user.username + '查看，系统将返还您' + str(
                        order_vip.order_mount) + '积分'
                    system_notice = SystemMessageModel.objects.filter(trade_no=order_vip.trade_no).first()
                    if not system_notice:
                        SystemMessageModel.objects.create(content=contented, sys_type='售出信息', user_id=fabu.user_id,
                                                          trade_no=order_vip.trade_no)
                    IntegralRecord.objects.create(integral_type='收获积分', integral=order_vip.order_mount,
                                                  user_id=fabu.user_id)
                    fabu_user = Users.objects.filter(id=fabu.user_id).first()
                    fabu_user.integration += 100
                    fabu_user.save()
                land_info = TransInfo.objects.filter(id=land_id)
                seria = DeliveryZhuanRangSerializers(land_info, many=True, context={'user_id': user.id})
                return Response({'status': '1', 'msg': '成功', 'data': seria.data, 'zc_data': zc_data})
            elif luyou == '/tudimessage/zhaoshang':
                land_info = AttractInfo.objects.filter(id=land_id)
                seria = DeliveryZhaoShangSerializers(land_info, many=True, context={'user_id': user.id})
                return Response({'status': '1', 'msg': '成功', 'data': seria.data, 'zc_data': zc_data})
            elif luyou in ['/activity/shalong', '/activity/yuebao', '/activity/tuijie', '/activity/kuanian']:
                activity_info = Activity.objects.filter(id=land_id)
                seria = DeliveryActivitySerializers(activity_info, many=True, context={'user_id': user.id})
                return Response({'status': '1', 'msg': '成功', 'data': seria.data, 'zc_data': zc_data})
            elif luyou in ['/tudilist/nadi', '/tudilist/gongdi', '/tudilist/shoulou', '/tudilist/loupan']:
                poplist_info = PropertyList.objects.filter(id=land_id)
                seria = DeliveryPopListSerializers(poplist_info, many=True, context={'user_id': user.id})
                return Response({'status': '1', 'msg': '成功', 'data': seria.data, 'zc_data': zc_data})
            elif luyou in ['/Investment/zhoubao', '/Investment/yuebao', '/Investment/jibao', '/Investment/bannianbao',
                           '/Investment/nianbao']:
                inv_info = InvestmentData.objects.filter(id=land_id)
                seria = DeliveryInvSerializers(inv_info, many=True, context={'user_id': user.id})
                return Response({'status': '1', 'msg': '成功', 'data': seria.data, 'zc_data': zc_data})

            else:

                return Response({'status': '0', 'msg': '路由错误'})
        else:
            return Response({'status': '0', 'msg': '无订单'})

    def post(self, request):
        user_id = request.data.get('user_id')
        land_id = request.data.get('land_id')
        luyou = request.data.get('luyou')
        zc = request.data.get('zc', 0)
        z_c = Zan.objects.filter(user_id=user_id, luyou=luyou, land_id=land_id).first()
        if z_c:
            z_c.zc = zc
            z_c.save()
        else:
            Zan.objects.create(user_id=user_id, luyou=luyou, land_id=land_id, zc=int(zc))

        return Response({'msg': '成功', 'status': '1'})


class CoordinatesView(APIView):

    def get(self, request):
        land_id = request.GET.get('land_id')
        luyou = request.GET.get('luyou')
        print(luyou)
        if luyou in ['/tudimessage/paimai', '/tudimessage/guapai', '/tudimessage/nitui']:
            land = LandInfo.objects.filter(id=land_id).first()
        elif luyou == '/tudimessage/zhuanrang':
            land = TransInfo.objects.filter(id=land_id).first()
        elif luyou == '/tudimessage/zhaoshang':
            land = AttractInfo.objects.filter(id=land_id).first()
        else:
            land = {'coordinates': '0'}
        return Response({'msg': '成功', 'status': '1', 'coordinates': land.coordinates,
                         'city': land.city, 'location': land.location, 'serial_number': land.serial_number})