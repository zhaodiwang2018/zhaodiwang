# -*- coding: utf-8 -*-
# @Time    : 2019/9/10 15:32
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : systemmessage.py
# @Software: PyCharm
from rest_framework.views import APIView, Response
from apps.index.models import *
from apps.land.serializers import *
from apps.user.models import *
from apps.land.forms import *
from apps.utils.mixin_utils import *
from rest_framework import serializers
import operator


class SystemMessageView(LoginRequiredMixin, APIView):
    # 新建系统通知
    def post(self, request):
        content = request.data.get('content')
        users = Users.objects.filter(is_admin=0)
        for user in users:
            try:

                SystemMessageModel.objects.create(content=content, sys_type='系统推送', user_id=user.id)
            except:
                return Response({'status': '0', 'msg': '系统消息发送失败'})
        return Response({'msg': '系统消息发送成功', 'status': '1'})


class BellNumber(LoginRequiredMixin, APIView):
    # 获取上方铃铛值
    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        if not user:
            return Response({'msg': '无此用户', 'status': '0'})
        # 系统消息总条数
        system_total_num = SystemMessageModel.objects.filter(user_id=user.id).count()
        # 系统消息已读条数
        system_is_read_num = SystemRead.objects.filter(user_id=user.id).count()
        # 系统消息未读消息
        system_no_read_num = system_total_num - system_is_read_num
        # 推送消息总条数
        push_total_num = YaoQing.objects.filter(user_id=user.id).count()
        # 推送消息已读条数
        push_is_read_num = YaoQingRead.objects.filter(user_id=user.id).count()
        # 推送消息未读条数
        push_no_read_num = push_total_num - push_is_read_num
        # 铃铛数
        bell_num = system_no_read_num + push_no_read_num
        push_nitui = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/nitui')
        if push_nitui:
            nitui_info_id = push_nitui.last().land_id
            nitui_info = LandInfo.objects.filter(id=nitui_info_id).first()
            nitui_city = nitui_info.city
        else:
            nitui_city = '无'
        push_nitui_list = []
        for push_nitui_read in push_nitui:
            n = YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=push_nitui_read.id)
            if n:
                push_nitui_list.append(n)

        push_paimai = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/paimai')
        if push_paimai:
            paimai_info_id = push_paimai.last().land_id
            paimai_info = LandInfo.objects.filter(id=paimai_info_id).first()
            paimai_city = paimai_info.city
        else:
            paimai_city = '无'
        push_paimai_list = []
        for push_paimai_read in push_paimai:
            n = YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=push_paimai_read.id)
            if n:
                push_paimai_list.append(n)
        push_guapai = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/guapai')
        if push_guapai:
            guapai_info_id = push_guapai.last().land_id
            guapai_info = LandInfo.objects.filter(id=guapai_info_id).first()
            guapai_city = guapai_info.city
        else:
            guapai_city = '无'
        push_guapai_list = []
        for push_guapai_read in push_guapai:
            g = YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=push_guapai_read.id)
            if g:
                push_guapai_list.append(g)
        push_zhuanrang = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/zhuanrang')
        if push_zhuanrang:
            zhuanrang_info_id = push_zhuanrang.last().land_id
            zhuanrang_info = TransInfo.objects.filter(id=zhuanrang_info_id).first()
            zhuanrang_city = zhuanrang_info.city
        else:
            zhuanrang_city = '无'
        push_zhuanrang_list = []
        for push_zhuanrang_read in push_zhuanrang:
            r = YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=push_zhuanrang_read.id)
            if r:
                push_zhuanrang_list.append(r)
        push_zhaoshang = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/zhaoshang')
        if push_zhaoshang:
            zhaoshang_info_id = push_zhaoshang.last().land_id
            zhaoshang_info = AttractInfo.objects.filter(id=zhaoshang_info_id).first()
            zhaoshang_city = zhaoshang_info.city
        else:
            zhaoshang_city = '无'
        push_zhaoshang_list = []
        for push_zhaoshang_read in push_zhaoshang:
            z = YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=push_zhaoshang_read.id)
            if z:
                push_zhaoshang_list.append(z)

        push_huodong = YaoQing.objects.filter(user_id=user.id,
                                              luyou__in=['/activity/shalong', '/activity/yuebao', '/activity/tuijie',
                                                         '/activity/kuanian'])
        push_huodong_list = []
        for push_huodong_read in push_huodong:
            h = YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=push_huodong_read.id)
            if h:
                push_huodong_list.append(h)
        push_bangdan = YaoQing.objects.filter(user_id=user.id,
                                              luyou__in=["/tudilist/nadi", "/tudilist/gongdi",
                                                         "/tudilist/shoulou",
                                                         "/tudilist/loupan"])
        push_bangdan_list = []
        for push_bangdan_read in push_bangdan:
            b = YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=push_bangdan_read.id)
            if b:
                push_bangdan_list.append(b)
        push_touzi = YaoQing.objects.filter(user_id=user.id,
                                            luyou__in=["/Investment/zhoubao", "/Investment/yuebao",
                                                       "/Investment/jibao", "/Investment/bannianbao",
                                                       "/Investment/nianbao"])
        push_touzi_list = []
        for push_touzi_read in push_touzi:
            t = YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=push_touzi_read.id)
            if t:
                push_touzi_list.append(t)
        return Response(
            {'bell_num': bell_num,'system_num': system_no_read_num, 'push_num': push_no_read_num,
             'nitui_no': push_nitui.count() - len(push_nitui_list),
             'gaupai_no': push_guapai.count() - len(push_guapai_list),
             'zhaoshang_no': push_zhaoshang.count() - len(push_zhaoshang_list),
             'paimai_no': push_paimai.count() - len(push_paimai_list),
             'zhuanrang_no': push_zhuanrang.count() - len(push_zhuanrang_list),
             'huodong_no': push_huodong.count() - len(push_huodong_list),
             'bangdan_no': push_bangdan.count() - len(push_bangdan_list),
             'touzi_no': push_touzi.count() - len(push_touzi_list),
             'nitui_city': nitui_city, 'paimai_city': paimai_city,
             'guapai_city': guapai_city, 'zhuanrang_city': zhuanrang_city,
             'zhaoshang_city': zhaoshang_city,
             'msg': '成功','status': '1'})


class SystemMessageSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = SystemMessageModel
        fields = ('content', 'create_on', 'is_read', 'sys_type')

    def get_is_read(self, obj):
        sys_read = SystemRead.objects.filter(id=obj.id, user_id=self.context['user_id'])
        if sys_read:
            return True
        return False


class BellListView(LoginRequiredMixin, APIView):

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        num_type = int(request.GET.get('num_type', 1))
        if num_type == 1:
            read_type = request.GET.get('read_type')
            if read_type == '2':
                activity_yaoqing = YaoQing.objects.filter(user_id=user.id,
                                                          luyou__in=['/activity/shalong', '/activity/yuebao',
                                                                     '/activity/tuijie', '/activity/kuanian'])
                for activity in activity_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=activity.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=activity.id)
            elif read_type == '1':
                land_yaoqing = YaoQing.objects.filter(user_id=user.id,
                                                      luyou__in=['/tudimessage/nitui', '/tudimessage/paimai',
                                                                 '/tudimessage/guapai', '/tudimessage/xiancheng',
                                                                 '/tudimessage/zhaoshang', '/tudimessage/zhuanrang'])
                for land in land_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=land.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=land.id)
            elif read_type == 'nitui':
                print(read_type)
                land_yaoqing = YaoQing.objects.filter(user_id=user.id,
                                                      luyou='/tudimessage/nitui')
                for land in land_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=land.id):
                        print(111)
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=land.id)
            elif read_type == 'paimai':
                land_yaoqing = YaoQing.objects.filter(user_id=user.id,
                                                      luyou='/tudimessage/paimai')
                for land in land_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=land.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=land.id)
            elif read_type == 'guapai':
                land_yaoqing = YaoQing.objects.filter(user_id=user.id,
                                                      luyou='/tudimessage/guapai')
                for land in land_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=land.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=land.id)
            elif read_type == 'zhaoshang':
                land_yaoqing = YaoQing.objects.filter(user_id=user.id,
                                                      luyou='/tudimessage/zhaoshang')
                for land in land_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=land.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=land.id)
            elif read_type == 'zhuanrang':
                land_yaoqing = YaoQing.objects.filter(user_id=user.id,
                                                      luyou='/tudimessage/zhuanrang')
                for land in land_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=land.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=land.id)
            elif read_type == '3':
                pop_yaoqing = YaoQing.objects.filter(user_id=user.id, luyou__in=["/tudilist/nadi", "/tudilist/gongdi",
                                                                                 "/tudilist/shoulou",
                                                                                 "/tudilist/loupan"])
                for pop in pop_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=pop.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=pop.id)
            elif read_type == '4':
                inv_yaoqing = YaoQing.objects.filter(user_id=user.id,
                                                     luyou__in=["/Investment/zhoubao", "/Investment/yuebao",
                                                                "/Investment/jibao", "/Investment/bannianbao",
                                                                "/Investment/nianbao"])
                for inv in inv_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=inv.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=inv.id)
            elif read_type == '5':
                all_yaoqing = YaoQing.objects.filter(user_id=user.id)
                for alls in all_yaoqing:
                    if not YaoQingRead.objects.filter(user_id=user.id, yaoqing_id=alls.id):
                        YaoQingRead.objects.create(user_id=user.id, yaoqing_id=alls.id)
            else:
                pass
            # nitui_obj = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/nitui')
            # nitui_seria = SelfLandInfoYaoqingTableSerializer(nitui_obj, many=True)
            # paimai_obj = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/paimai')
            # paimai_seria = SelfLandInfoYaoqingTableSerializer(paimai_obj, many=True)
            # guapai_obj = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/guapai')
            # guapai_seria = SelfLandInfoYaoqingTableSerializer(guapai_obj, many=True)
            # trans_obj = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/zhuanrang')
            # trans_seria = SelfTransInfoYaoqingSerializer(trans_obj, many=True)
            #
            # attract_obj = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/zhaoshang')
            # attract_seria = SelfAttractYaoqingSerializer(attract_obj, many=True)
            #
            # activity_obj = YaoQing.objects.filter(user_id=user.id, luyou__in=['/activity/shalong', '/activity/yuebao',
            #                                                             '/activity/tuijie', '/activity/kuanian'])
            # activity_seria = ActivityYaoqingSerializers(activity_obj, many=True)
            # property_obj = YaoQing.objects.filter(user_id=user.id,
            #                                       luyou__in=["/tudilist/nadi", "/tudilist/gongdi", "/tudilist/shoulou",
            #                                                  "/tudilist/loupan"])
            # property_seria = PropertyListYaoqingSerializers(property_obj, many=True)
            # inv_obj = YaoQing.objects.filter(user_id=user.id, luyou__in=["/Investment/zhoubao", "/Investment/yuebao",
            #                                                        "/Investment/jibao", "/Investment/bannianbao",
            #                                                        "/Investment/nianbao"])
            # inv_seria = InvestmentDataYaoqingSerializers(inv_obj, many=True)
            # nitui_data = sorted(nitui_seria.data, key=operator.itemgetter('create_on'), reverse=True)
            # paimai_data = sorted(paimai_seria.data, key=operator.itemgetter('create_on'), reverse=True)
            #
            # gaupai_data = sorted(guapai_seria.data, key=operator.itemgetter('create_on'), reverse=True)
            # trans_data = sorted(trans_seria.data, key=operator.itemgetter('create_on'), reverse=True)
            # attract_data = sorted(attract_seria.data, key=operator.itemgetter('create_on'), reverse=True)
            #
            # activity_data = sorted(activity_seria.data, key=operator.itemgetter('create_on'), reverse=True)
            #
            # property_data = sorted(property_seria.data, key=operator.itemgetter('create_on'), reverse=True)
            #
            # inv_data = sorted(inv_seria.data, key=operator.itemgetter('create_on'), reverse=True)
            #
            # return Response({'msg': '获取成功', 'status': '1', 'trans_data': trans_data, 'attract_data': attract_data,
            #                  'activity_data': activity_data, 'property_data': property_data, 'inv_data': inv_data
            #                  , 'nitui_data': nitui_data, 'paimai_data': paimai_data, 'gaupai_data': gaupai_data})
            land_obj = YaoQing.objects.filter(user_id=user.id, luyou__in=['/tudimessage/nitui', '/tudimessage/paimai',
                                                                          '/tudimessage/guapai',
                                                                          '/tudimessage/xiancheng'])
            land_seria = SelfLandInfoYaoqingTableSerializer(land_obj, many=True)
            trans_obj = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/zhuanrang')
            trans_seria = SelfTransInfoYaoqingSerializer(trans_obj, many=True)

            attract_obj = YaoQing.objects.filter(user_id=user.id, luyou='/tudimessage/zhaoshang')
            attract_seria = SelfAttractYaoqingSerializer(attract_obj, many=True)

            activity_obj = YaoQing.objects.filter(user_id=user.id, luyou__in=['/activity/shalong', '/activity/yuebao',
                                                                              '/activity/tuijie', '/activity/kuanian'])
            activity_seria = ActivityYaoqingSerializers(activity_obj, many=True)
            property_obj = YaoQing.objects.filter(user_id=user.id,
                                                  luyou__in=["/tudilist/nadi", "/tudilist/gongdi", "/tudilist/shoulou",
                                                             "/tudilist/loupan"])
            property_seria = PropertyListYaoqingSerializers(property_obj, many=True)
            inv_obj = YaoQing.objects.filter(user_id=user.id, luyou__in=["/Investment/zhoubao", "/Investment/yuebao",
                                                                         "/Investment/jibao", "/Investment/bannianbao",
                                                                         "/Investment/nianbao"])
            inv_seria = InvestmentDataYaoqingSerializers(inv_obj, many=True)
            data = land_seria.data + trans_seria.data + activity_seria.data + attract_seria.data + property_seria.data + inv_seria.data
            data = sorted(data, key=operator.itemgetter('create_on'), reverse=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': data})
        elif num_type == 2:
            page = int(request.GET.get('page'))
            objs = SystemMessageModel.objects.filter(user_id=user.id).order_by('-create_on')
            seria = SystemMessageSerializer(objs, many=True, context={'user_id': user.id})
            for obj in objs:
                if not SystemRead.objects.filter(user_id=user.id, sys_id=obj.id):
                    try:
                        SystemRead.objects.create(user_id=user.id, sys_id=obj.id)
                    except:
                        return Response({'status': '0', 'msg': '已读创建失败'})
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data[(page - 1) * 10:(page - 1) * 10 + 10]})
