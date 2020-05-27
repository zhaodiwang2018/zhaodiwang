from rest_framework.views import APIView, Response
from apps.land.serializers import *
from apps.land.forms import *
from apps.user.models import *
from apps.utils.mixin_utils import *
import re
import datetime
import pytz


# TODO：手机全部列表页
# class MobileLandView(APIView):
#
#     def get(self, request):
#
#         info = request.GET.get('info', '/tudimessage/zhuanrang')
#         page = int(request.GET.get('page'))
#         if not info:
#             return Response({'msg': 'info没传', 'status': '0'})
#         if info == '/tudimessage/nitui':
#             land_info = LandInfo.objects.filter(land_type=2, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = LandSerializers(land_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/tudimessage/paimai':
#             land_info = LandInfo.objects.filter(land_type=3, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = LandSerializers(land_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/tudimessage/guapai':
#             land_info = LandInfo.objects.filter(land_type=1, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = LandSerializers(land_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/tudimessage/xiancheng':
#             land_info = LandInfo.objects.filter(land_type=4, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = LandSerializers(land_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/tudimessage/zhuanrang':
#             trans_info = TransInfo.objects.filter(audit_state=2).order_by('-id')[:5]
#             seria = TransSerializers(trans_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/tudimessage/zhaoshang':
#             attract_info = AttractInfo.objects.filter(audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = AttractSerializers(attract_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/activity/shalong':
#             activity_info = Activity.objects.filter(activity_type=1, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = ActivityListSerializers(activity_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/activity/yuebao':
#             activity_info = Activity.objects.filter(activity_type=2, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = ActivityListSerializers(activity_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/activity/tuijie':
#             activity_info = Activity.objects.filter(activity_type=3, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = ActivityListSerializers(activity_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == '/activity/kuanian':
#             activity_info = Activity.objects.filter(activity_type=4, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = ActivityListSerializers(activity_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/tudilist/nadi":
#             property_info = PropertyList.objects.filter(property_type=1, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = PropertyListSerializers(property_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/tudilist/gongdi":
#             property_info = PropertyList.objects.filter(property_type=2, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = PropertyListSerializers(property_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/tudilist/shoulou":
#             property_info = PropertyList.objects.filter(property_type=3, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = PropertyListSerializers(property_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/tudilist/loupan":
#             property_info = PropertyList.objects.filter(property_type=4, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = PropertyListSerializers(property_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/Investment/zhoubao":
#             inv_info = InvestmentData.objects.filter(property_type=1, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = InvestmentDataSerializers(inv_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/Investment/yuebao":
#             inv_info = InvestmentData.objects.filter(property_type=2, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = InvestmentDataSerializers(inv_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/Investment/jibao":
#             inv_info = InvestmentData.objects.filter(property_type=3, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = InvestmentDataSerializers(inv_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/Investment/bannianbao":
#             inv_info = InvestmentData.objects.filter(property_type=4, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = InvestmentDataSerializers(inv_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         elif info == "/Investment/nianbao":
#             inv_info = InvestmentData.objects.filter(property_type=5, audit_state=2).order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
#             seria = InvestmentDataSerializers(inv_info, many=True)
#             return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
#         else:
#             return Response({'msg': '路径传错了', 'status': '0'})


# TODO：pc全部列表页
class LandView(LoginRequiredMixin, APIView):

    def get(self, request):
        # page = int(request.GET.get('page'))
        info = request.GET.get('info', '/tudimessage/zhuanrang')
        if not info:
            return Response({'msg': 'info没传', 'status': '0'})
        if info == '/tudimessage/nitui':
            land_info = LandInfo.objects.filter(land_type=2, audit_state=2).order_by('-id')[:5]
            seria = LandSerializers(land_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/tudimessage/paimai':
            land_info = LandInfo.objects.filter(land_type=3, audit_state=2).order_by('-id')[:5]
            seria = LandSerializers(land_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/tudimessage/guapai':
            land_info = LandInfo.objects.filter(land_type=1, audit_state=2).order_by('-id')[:5]
            seria = LandSerializers(land_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/tudimessage/xiancheng':
            land_info = LandInfo.objects.filter(land_type=4, audit_state=2).order_by('-id')[:5]
            seria = LandSerializers(land_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/tudimessage/zhuanrang':
            trans_info = TransInfo.objects.filter(audit_state=2).order_by('-id')[:5]
            seria = TransSerializers(trans_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/tudimessage/zhaoshang':
            attract_info = AttractInfo.objects.filter(audit_state=2).order_by('-id')[:5]
            seria = AttractSerializers(attract_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/activity/shalong':
            activity_info = Activity.objects.filter(activity_type=1, audit_state=2).order_by('-id')[:5]
            seria = ActivityListSerializers(activity_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/activity/yuebao':
            activity_info = Activity.objects.filter(activity_type=2, audit_state=2).order_by('-id')[:5]
            seria = ActivityListSerializers(activity_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/activity/tuijie':
            activity_info = Activity.objects.filter(activity_type=3, audit_state=2).order_by('-id')[:5]
            seria = ActivityListSerializers(activity_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == '/activity/kuanian':
            activity_info = Activity.objects.filter(activity_type=4, audit_state=2).order_by('-id')[:5]
            seria = ActivityListSerializers(activity_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/tudilist/nadi":
            property_info = PropertyList.objects.filter(property_type=1, audit_state=2).order_by('-id')[:5]
            seria = PropertyListSerializers(property_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/tudilist/gongdi":
            property_info = PropertyList.objects.filter(property_type=2, audit_state=2).order_by('-id')[:5]
            seria = PropertyListSerializers(property_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/tudilist/shoulou":
            property_info = PropertyList.objects.filter(property_type=3, audit_state=2).order_by('-id')[:5]
            seria = PropertyListSerializers(property_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/tudilist/loupan":
            property_info = PropertyList.objects.filter(property_type=4, audit_state=2).order_by('-id')[:5]
            seria = PropertyListSerializers(property_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/Investment/zhoubao":
            inv_info = InvestmentData.objects.filter(property_type=1, audit_state=2).order_by('-id')[:5]
            seria = InvestmentDataSerializers(inv_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/Investment/yuebao":
            inv_info = InvestmentData.objects.filter(property_type=2, audit_state=2).order_by('-id')[:5]
            seria = InvestmentDataSerializers(inv_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/Investment/jibao":
            inv_info = InvestmentData.objects.filter(property_type=3, audit_state=2).order_by('-id')[:5]
            seria = InvestmentDataSerializers(inv_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/Investment/bannianbao":
            inv_info = InvestmentData.objects.filter(property_type=4, audit_state=2).order_by('-id')[:5]
            seria = InvestmentDataSerializers(inv_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        elif info == "/Investment/nianbao":
            inv_info = InvestmentData.objects.filter(property_type=5, audit_state=2).order_by('-id')[:5]
            seria = InvestmentDataSerializers(inv_info, many=True)
            return Response({'data': seria.data, 'msg': '获取成功', 'status': '1'})
        else:
            return Response({'msg': '路径传错了', 'status': '0'})


# TODO：全部详情页
class LandDetailView(LoginRequiredMixin, APIView):

    # 获取查看人数
    def get_receive_peo(self, luyou, land_id, user_id):
        obj = ReceivePeo.objects.filter(luyou=luyou, user_id=user_id, information_id=land_id).first()
        if not obj:
            ReceivePeo.objects.create(user_id=user_id, luyou=luyou, information_id=land_id)
        return ReceivePeo.objects.filter(luyou=luyou, information_id=land_id).count()

    # 获取是否收藏
    def get_is_collection(self, luyou, land_id, user_id):
        res = Collection.objects.filter(luyou=luyou, user_id=user_id, information_id=land_id, ).first()
        if res:
            collection = True
        else:
            collection = False
        return collection

    # 获取是否已支付
    def get_is_pay(self, luyou, land_id, user_id):
        res = OrderInfo.objects.filter(user_id=user_id, luyou=luyou, land_id=land_id,
                                       pay_status='TRADE_SUCCESS').first()
        if res:
            pay = True
        else:
            pay = False
        return pay

    # 此刻是否vip
    def get_is_vip(self, user_id):
        vip = VipExpire.objects.filter(user_id=user_id).first()
        if vip:
            if vip.expire_time.replace(tzinfo=pytz.timezone('UTC')) > datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')):
                return True
            return False
        return False
    # 获取所有用户的数量
    def get_users(self):
        return Users.objects.all().count()


    # 获取该地区的所有用户数
    def get_city_users(self, city):
        num = 0
        for user in Users.objects.all():
            if user.city:
                b = re.sub(r'\'', '', user.city)
                c = re.sub(r'\[', '', b)
                d = re.sub(r'\]', '', c)
                e = d
                if city in e:
                    num += 1
        return num
    def get_add_chakan_num(self):
        today = datetime.date.today()
        today_data = AdminUserChart.objects.filter(create_on=today).first()
        if today_data:
            today_data.today_chakan += 1
            today_data.save()
        else:
            user_num = Users.objects.count()
            AdminUserChart.objects.create(today_chakan=1, user_all=user_num)

    def get_add_chakan_active(self, user_id):
        user = Users.objects.filter(id=user_id).first()
        if user.usertype == '1':
            user_rank = PaiMing.objects.filter(user_id=user_id).first()
            user_rank.act_num += 0.5
            user_rank.save()

    def get(self, request):

        luyou = request.GET.get('luyou', '/tudimessage/zhuanrang')
        land_id = request.GET.get("land_id", 13)
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        user_id = user.id
        if not land_id:
            return Response({'msg': 'id没传', 'status': '0'})
        if not luyou:
            return Response({'msg': 'info没传', 'status': '0'})

        if luyou == '/tudimessage/zhuanrang':
            # if charge:
            #     if charge.zhuanrang > 0:
            #         is_charge_num = True
            #         charge_num = charge.zhuanrang
            #     else:
            #         is_charge_num = False
            #         charge_num = 0
            # else:
            #     charge_num = 0
            #     is_charge_num = False
            pay = self.get_is_pay(luyou, land_id, user_id)
            trans_info_list = TransInfo.objects.filter(audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = TransSerializers(trans_info_list, many=True)
            trans_info = TransInfo.objects.filter(id=land_id, audit_state=2)
            if not trans_info:
                return Response({'status': '0', 'msg': '无'})
            seria = TransDetailSerializers(trans_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            is_vip = self.get_is_vip(user_id)
            users = self.get_city_users(trans_info[0].city)
            user.login_num += 1
            user.save()
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == '/tudimessage/zhaoshang':
            attract_info_list = AttractInfo.objects.filter(audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = AttractSerializers(attract_info_list, many=True)
            attract_info = AttractInfo.objects.filter(id=land_id, audit_state=2)
            if not attract_info:
                return Response({'status': '0', 'msg': '无'})
            seria = AttractDetailSerializers(attract_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_city_users(attract_info[0].city)
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)
            # 文章查看次数+1
            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == '/activity/shalong':
            activity_info_list = Activity.objects.filter(audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = ActivityListSerializers(activity_info_list, many=True)
            activity_info = Activity.objects.filter(id=land_id, audit_state=2)
            if not activity_info:
                return Response({'status': '0', 'msg': '无'})
            seria = ActivityDetailSerializers(activity_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)
            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == '/activity/yuebao':
            activity_info_list = Activity.objects.filter(audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = ActivityListSerializers(activity_info_list, many=True)
            activity_info = Activity.objects.filter(id=land_id, audit_state=2)
            if not activity_info:
                return Response({'status': '0', 'msg': '无'})
            seria = ActivityDetailSerializers(activity_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)
            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == '/activity/tuijie':

            activity_info_list = Activity.objects.filter(audit_state=2).exclude(id=land_id).order_by('-id')[0:3]
            seria_list = ActivityListSerializers(activity_info_list, many=True)
            activity_info = Activity.objects.filter(id=land_id, audit_state=2)
            if not activity_info:
                return Response({'status': '0', 'msg': '无'})
            seria = ActivityDetailSerializers(activity_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection, 'receive_peo': receive_peo,
                 'pay': pay, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == '/activity/kuanian':

            activity_info_list = Activity.objects.filter(audit_state=2).exclude(id=land_id).order_by('-id')[0:3]
            seria_list = ActivityListSerializers(activity_info_list, many=True)
            activity_info = Activity.objects.filter(id=land_id, audit_state=2)
            if not activity_info:
                return Response({'status': '0', 'msg': '无'})
            seria = ActivityDetailSerializers(activity_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == '/tudimessage/nitui':
            land_info_list = LandInfo.objects.filter(land_type='2', audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = LandSerializers(land_info_list, many=True)
            land_info = LandInfo.objects.filter(id=land_id, audit_state=2)
            if not land_info:
                return Response({'status': '0', 'msg': '无'})
            seria = LandDetailSerializers(land_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_city_users(land_info[0].city)
            is_vip = self.get_is_vip(user_id)
            user.login_num += 1
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == '/tudimessage/paimai':
            land_info_list = LandInfo.objects.filter(land_type='3', audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = LandSerializers(land_info_list, many=True)
            land_info = LandInfo.objects.filter(id=land_id, audit_state=2)
            if not land_info:
                return Response({'status': '0', 'msg': '无'})
            seria = LandDetailSerializers(land_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_city_users(land_info[0].city)
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == '/tudimessage/guapai':
            land_info_list = LandInfo.objects.filter(land_type='1', audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = LandSerializers(land_info_list, many=True)
            land_info = LandInfo.objects.filter(id=land_id, audit_state=2)
            if not land_info:
                return Response({'status': '0', 'msg': '无'})
            seria = LandDetailSerializers(land_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_city_users(land_info[0].city)
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == '/tudimessage/xiancheng':
            land_info_list = LandInfo.objects.filter(land_type='4', audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = LandSerializers(land_info_list, many=True)
            land_info = LandInfo.objects.filter(id=land_id, audit_state=2)
            if not land_info:
                return Response({'status': '0', 'msg': '无'})
            seria = LandDetailSerializers(land_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_city_users(land_info[0].city)
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == "/tudilist/nadi":
            property_info_list = PropertyList.objects.filter(property_type=1, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = PropertyListSerializers(property_info_list, many=True)
            property_info = PropertyList.objects.filter(id=land_id, audit_state=2)
            if not property_info:
                return Response({'status': '0', 'msg': '无'})
            seria = PropertyListDetailSerializers(property_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == "/tudilist/gongdi":
            property_info_list = PropertyList.objects.filter(property_type=2, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = PropertyListSerializers(property_info_list, many=True)
            property_info = PropertyList.objects.filter(id=land_id, audit_state=2)
            if not property_info:
                return Response({'status': '0', 'msg': '无'})
            seria = PropertyListDetailSerializers(property_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == "/tudilist/shoulou":
            property_info_list = PropertyList.objects.filter(property_type=3, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = PropertyListSerializers(property_info_list, many=True)
            property_info = PropertyList.objects.filter(id=land_id, audit_state=2)
            if not property_info:
                return Response({'status': '0', 'msg': '无'})
            seria = PropertyListDetailSerializers(property_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == "/tudilist/loupan":
            property_info_list = PropertyList.objects.filter(property_type=4, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = PropertyListSerializers(property_info_list, many=True)
            property_info = PropertyList.objects.filter(id=land_id, audit_state=2)
            if not property_info:
                return Response({'status': '0', 'msg': '无'})
            seria = PropertyListDetailSerializers(property_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == "/Investment/zhoubao":
            inv_info_list = InvestmentData.objects.filter(property_type=1, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = InvestmentDataSerializers(inv_info_list, many=True)
            inv_info = InvestmentData.objects.filter(id=land_id, audit_state=2)
            if not inv_info:
                return Response({'status': '0', 'msg': '无'})
            seria = InvestmentDataDetailSerializers(inv_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})

        elif luyou == "/Investment/yuebao":
            inv_info_list = InvestmentData.objects.filter(property_type=2, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = InvestmentDataSerializers(inv_info_list, many=True)
            inv_info = InvestmentData.objects.filter(id=land_id, audit_state=2)
            if not inv_info:
                return Response({'status': '0', 'msg': '无'})
            seria = InvestmentDataDetailSerializers(inv_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == "/Investment/jibao":
            inv_info_list = InvestmentData.objects.filter(property_type=3, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = InvestmentDataSerializers(inv_info_list, many=True)
            inv_info = InvestmentData.objects.filter(id=land_id, audit_state=2)
            if not inv_info:
                return Response({'status': '0', 'msg': '无'})
            seria = InvestmentDataDetailSerializers(inv_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == "/Investment/bannianbao":
            inv_info_list = InvestmentData.objects.filter(property_type=4, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = InvestmentDataSerializers(inv_info_list, many=True)
            inv_info = InvestmentData.objects.filter(id=land_id, audit_state=2)
            if not inv_info:
                return Response({'status': '0', 'msg': '无'})
            seria = InvestmentDataDetailSerializers(inv_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        elif luyou == "/Investment/nianbao":
            inv_info_list = InvestmentData.objects.filter(property_type=5, audit_state=2).exclude(id=land_id).order_by('-id')[:3]
            seria_list = InvestmentDataSerializers(inv_info_list, many=True)
            inv_info = InvestmentData.objects.filter(id=land_id, audit_state=2)
            if not inv_info:
                return Response({'status': '0', 'msg': '无'})
            seria = InvestmentDataDetailSerializers(inv_info, many=True)
            receive_peo = self.get_receive_peo(luyou, land_id, user_id)
            collection = self.get_is_collection(luyou, land_id, user_id)
            pay = self.get_is_pay(luyou, land_id, user_id)
            users = self.get_users()
            is_vip = self.get_is_vip(user_id)
            self.get_add_chakan_num()
            self.get_add_chakan_active(user_id)

            user.login_num += 1
            user.save()
            return Response(
                {'data': seria.data, 'data_list': seria_list.data, 'collection': collection,
                 'receive_peo': receive_peo, 'pay': pay, 'is_vip': is_vip, 'users': users, 'msg': '获取成功', 'status': '1'})
        else:
            return Response({'msg': '路径传错了', 'status': '0'})
