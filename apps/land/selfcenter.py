from rest_framework.views import APIView, Response
from apps.land.serializers import *
from apps.land.forms import *
from apps.user.models import *
from apps.utils.mixin_utils import *
import datetime
from datetime import timezone
import pytz
import operator

import time


# TODO:个人中心右侧记录
class RecordView(LoginRequiredMixin, APIView):
    def get(self, request):
        user_id = request.GET.get('user_id', 1)
        info = request.GET.get('info', 'userinfo3')
        if info == 'userinfo3':
            land = ReceivePeo.objects.filter(user_id=user_id,
                                             luyou__in=['/tudimessage/nitui', '/tudimessage/paimai',
                                                        '/tudimessage/guapai', '/tudimessage/xiancheng',
                                                        '/tudimessage/zhuanrang', '/tudimessage/zhaoshang']).order_by(
                'create_on')
            record = []
            for land_id in land:
                if land_id.luyou == '/tudimessage/zhuanrang':
                    trans = TransInfo.objects.filter(id=land_id.information_id, audit_state=2)
                    if trans:
                        seria = TransSerializers(trans, many=True)
                        record.append(seria.data[0])
                elif land_id.luyou == '/tudimessage/zhaoshang':
                    attract = AttractInfo.objects.filter(id=land_id.information_id, audit_state=2)
                    if attract:
                        seria = AttractSerializers(attract, many=True)
                        record.append(seria.data[0])
                elif land_id.luyou == '/tudimessage/nitui' or land_id.luyou == '/tudimessage/paimai' or land_id.luyou == '/tudimessage/guapai' or land_id.luyou == '/tudimessage/xiancheng':
                    lands = LandInfo.objects.filter(id=land_id.information_id, audit_state=2)
                    if lands:
                        seria = LandSerializers(lands, many=True)
                        record.append(seria.data[0])
            return Response({'msg': '成功', 'status': '1', 'data': record})
        elif info == 'userinfo1':

            land = ReceivePeo.objects.filter(user_id=user_id).order_by('create_on')
            record = []
            for land_id in land:
                if land_id.luyou == '/tudimessage/zhuanrang':
                    trans = TransInfo.objects.filter(id=land_id.information_id, audit_state=2)
                    if trans:
                        seria = TransSerializers(trans, many=True)
                        record.append(seria.data[0])
                elif land_id.luyou == '/tudimessage/zhaoshang':
                    attract = AttractInfo.objects.filter(id=land_id.information_id, audit_state=2)
                    if attract:
                        seria = AttractSerializers(attract, many=True)
                        record.append(seria.data[0])
                elif land_id.luyou == '/tudimessage/nitui' or land_id.luyou == '/tudimessage/paimai' or land_id.luyou == '/tudimessage/guapai' or land_id.luyou == '/tudimessage/xiancheng':
                    lands = LandInfo.objects.filter(id=land_id.information_id, audit_state=2)
                    if lands:
                        seria = LandSerializers(lands, many=True)
                        record.append(seria.data[0])
                elif land_id.luyou in ["/Investment/zhoubao", "/Investment/yuebao", "/Investment/jibao",
                                       "/Investment/bannnianbao", "/Investment/nianbao"]:
                    lands = InvestmentData.objects.filter(id=land_id.information_id, audit_state=2)
                    if lands:
                        seria = InvestmentDataSerializers(lands, many=True)
                        record.append(seria.data[0])
                elif land_id.luyou in ['/activity/shalong', '/activity/yuebao', '/activity/tuijie',
                                       '/activity/kuanian']:
                    lands = Activity.objects.filter(id=land_id.information_id, audit_state=2)
                    if lands:
                        seria = ActivityListSerializers(lands, many=True)
                        record.append(seria.data[0])
                elif land_id.luyou in ["/tudilist/nadi", "/tudilist/gongdi", "/tudilist/shoulou", "/tudilist/loupan"]:
                    lands = PropertyList.objects.filter(id=land_id.information_id, audit_state=2)
                    if lands:
                        seria = PropertyListSerializers(lands, many=True)
                        record.append(seria.data[0])
            return Response({'msg': '成功', 'status': '1', 'data': record})
        elif info == 'userinfo2':
            user = Users.objects.filter(id=user_id).first()
            expire = VipExpire.objects.filter(user_id=user_id).first()
            consumption = OrderInfo.objects.filter(user_id=user_id, pay_status='TRADE_SUCCESS').order_by('-id')
            consumption_data = ConsumptionSerializers(consumption, many=True)
            if expire:
                days = expire.expire_time.replace(tzinfo=pytz.timezone('UTC')) - datetime.datetime.now(timezone.utc)
                if expire.expire_time.replace(tzinfo=pytz.timezone('UTC')) < datetime.datetime.now(timezone.utc):
                    return Response({'msg': '过期', 'status': '0'})
                # TODO:剩余条数查看，删除！！！
                chargenum = ChargeNumber.objects.filter(user_id=user_id)
                seria = ChargeNumberSerializers(chargenum, many=True)
                return Response(
                    {'vip_num': user.vip_num, 'days': days.days, 'expire': expire.expire_time, 'num_data': seria.data,
                     'consumption_data': consumption_data.data, 'msg': '成功', 'status': '1'})

            return Response(
                {'vip_num': user.vip_num, 'consumption_data': consumption_data.data, 'msg': '成功', 'status': '1'})
        elif info == 'userinfo4':
            activity = ReceivePeo.objects.filter(user_id=user_id,
                                                 luyou__in=['/activity/shalong', '/activity/yuebao', '/activity/tuijie',
                                                            '/activity/kuanian']).order_by('create_on')
            record = []
            for land_id in activity:
                lands = Activity.objects.filter(id=land_id.information_id, audit_state=2)
                if lands:
                    seria = ActivityListSerializers(lands, many=True)
                    record.append(seria.data[0])
            return Response({'msg': '成功', 'status': '1', 'data': record})
        elif info == 'userinfo5':
            record = []
            proper = ReceivePeo.objects.filter(user_id=user_id,
                                               luyou__in=["/tudilist/nadi", "/tudilist/gongdi", "/tudilist/shoulou",
                                                          "/tudilist/loupan"]).order_by('create_on')
            for land_id in proper:
                lands = PropertyList.objects.filter(id=land_id.information_id, audit_state=2)
                if lands:
                    seria = PropertyListSerializers(lands, many=True)
                    record.append(seria.data[0])

            return Response({'msg': '成功', 'status': '1', 'data': record})
        elif info == 'userinfo6':
            investment = ReceivePeo.objects.filter(user_id=user_id,
                                                   luyou__in=["/Investment/zhoubao", "/Investment/yuebao",
                                                              "/Investment/jibao", "/Investment/bannnianbao",
                                                              "/Investment/nianbao"]).order_by('create_on')
            record = []
            for land_id in investment:
                lands = InvestmentData.objects.filter(id=land_id.information_id, audit_state=2)
                if lands:
                    seria = InvestmentDataSerializers(lands, many=True)
                    record.append(seria.data[0])

            return Response({'msg': '成功', 'status': '1', 'data': record})
        elif info == 'userinfo8':
            return Response({'msg': '获取成功', 'status': '1'})
        return Response({'msg': 'erro', 'status': '0', })


# TODO：个人中心数据
class SelfNumber(LoginRequiredMixin, APIView):

    def get_today_str(self):
        return time.mktime(datetime.date.today().timetuple())

    def get_weak_first_str(self):
        today = datetime.date.today()
        dayscount = datetime.timedelta(days=today.isoweekday())
        dayto = today - dayscount
        return time.mktime(datetime.datetime(dayto.year, dayto.month, dayto.day).timetuple())

    def get_weak_last_str(self):
        today = datetime.date.today()
        dayscount = datetime.timedelta(days=today.isoweekday())
        dayto = today - dayscount
        sixdays = datetime.timedelta(days=7)
        dayfrom = dayto + sixdays
        return time.mktime(datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day).timetuple())

    def get_month_first_str(self):
        return time.mktime(datetime.datetime(datetime.date.today().year, datetime.date.today().month, 1).timetuple())

    def get_month_last_str(self):
        return time.mktime((datetime.datetime(datetime.date.today().year, datetime.date.today().month + 1,
                                              1) - datetime.timedelta(1)).timetuple())
    def get_year_first_str(self):
        return time.mktime(datetime.datetime(datetime.date.today().year, 1, 1).timetuple())

    def get_year_last_str(self):
        return time.mktime(datetime.datetime(datetime.date.today().year, 12, 31).timetuple())

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        user_id = user.id
        info = request.GET.get('info', 'userinfo8')
        data = {}
        nitui_collection_num = Collection.objects.filter(luyou='/tudimessage/nitui', user_id=user_id, ).count()
        paimai_collection_num = Collection.objects.filter(luyou='/tudimessage/paimai', user_id=user_id, ).count()
        guapai_collection_num = Collection.objects.filter(luyou='/tudimessage/guapai', user_id=user_id, ).count()
        zhuanrang_collection_num = Collection.objects.filter(luyou='/tudimessage/zhuanrang', user_id=user_id, ).count()
        zhaoshang_collection_num = Collection.objects.filter(luyou='/tudimessage/zhaoshang', user_id=user_id, ).count()
        xiancheng_collection_num = Collection.objects.filter(luyou='/tudimessage/xiancheng', user_id=user_id, ).count()
        nitui_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/nitui', user_id=user_id, ).count()
        paimai_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/paimai', user_id=user_id, ).count()
        guapai_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/guapai', user_id=user_id, ).count()
        zhuanrang_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/zhuanrang', user_id=user_id, ).count()
        zhaoshang_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/zhaoshang', user_id=user_id, ).count()
        xiancheng_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/xiancheng', user_id=user_id, ).count()
        # 活动收藏
        shalong_collection_num = Collection.objects.filter(luyou='/activity/shalong', user_id=user_id, ).count()
        yuebao_collection_num = Collection.objects.filter(luyou='/activity/yuebao', user_id=user_id, ).count()
        tuijie_collection_num = Collection.objects.filter(luyou='/activity/tuijie', user_id=user_id, ).count()
        # 活动查看
        shalong_receive_num = ReceivePeo.objects.filter(luyou='/activity/shalong', user_id=user_id, ).count()
        yue_receive_num = ReceivePeo.objects.filter(luyou='/activity/yuebao', user_id=user_id, ).count()
        tuijie_receive_num = ReceivePeo.objects.filter(luyou='/activity/tuijie', user_id=user_id, ).count()

        nadi_collection_num = Collection.objects.filter(luyou="/tudilist/nadi", user_id=user_id, ).count()
        gongdi_collection_num = Collection.objects.filter(luyou='/tudilist/gongdi', user_id=user_id, ).count()
        shoulou_collection_num = Collection.objects.filter(luyou='/tudilist/shoulou', user_id=user_id, ).count()
        loupan_collection_num = Collection.objects.filter(luyou='/tudilist/loupan', user_id=user_id, ).count()
        nadi_receive_num = ReceivePeo.objects.filter(luyou="/tudilist/nadi", user_id=user_id, ).count()
        gongdi_receive_num = ReceivePeo.objects.filter(luyou='/tudilist/gongdi', user_id=user_id, ).count()
        shoulou_receive_num = ReceivePeo.objects.filter(luyou='/tudilist/shoulou', user_id=user_id, ).count()
        loupan_receive_num = ReceivePeo.objects.filter(luyou='/tudilist/loupan', user_id=user_id, ).count()
        zhoubao_collection_num = Collection.objects.filter(luyou="/Investment/zhoubao", user_id=user_id, ).count()
        yue_collection_num = Collection.objects.filter(luyou="/Investment/yuebao", user_id=user_id, ).count()
        jibao_collection_num = Collection.objects.filter(luyou="/Investment/jibao", user_id=user_id, ).count()
        bannianbao_collection_num = Collection.objects.filter(luyou="/Investment/bannianbao", user_id=user_id, ).count()
        nianbao_collection_num = Collection.objects.filter(luyou="/Investment/nianbao", user_id=user_id, ).count()
        zhoubao_receive_num = ReceivePeo.objects.filter(luyou="/Investment/zhoubao", user_id=user_id, ).count()
        yuebao_receive_num = ReceivePeo.objects.filter(luyou="/Investment/yuebao", user_id=user_id, ).count()
        jibao_receive_num = ReceivePeo.objects.filter(luyou="/Investment/jibao", user_id=user_id, ).count()
        bannianbao_receive_num = ReceivePeo.objects.filter(luyou="/Investment/bannianbao", user_id=user_id, ).count()
        nianbao_receive_num = ReceivePeo.objects.filter(luyou="/Investment/nianbao", user_id=user_id, ).count()
        # 被联系
        paimai_contacted_num = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/paimai').count()

        zhuanrang_contacted_num = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/zhuanrang').count()
        zhaoshang_contacted_num = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/zhaoshang').count()

        xiancheng_contacted_num = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/nitui').count()

        # 联系
        nitui_contact_num = Contact.objects.filter(luyou='/tudimessage/nitui', user_id=user_id, ).count()
        paimai_contact_num = Contact.objects.filter(luyou='/tudimessage/paimai', user_id=user_id, ).count()
        guapai_contact_num = Contact.objects.filter(luyou='/tudimessage/guapai', user_id=user_id, ).count()
        zhuanrang_contact_num = Contact.objects.filter(luyou='/tudimessage/zhuanrang', user_id=user_id, ).count()
        zhaoshang_contact_num = Contact.objects.filter(luyou='/tudimessage/zhaoshang', user_id=user_id, ).count()
        xiancheng_contact_num = Contact.objects.filter(luyou='/tudimessage/xiancheng', user_id=user_id, ).count()
        # 发布
        fabu_num = ReleaseRecord.objects.filter(user_id=user_id).count()
        # 报名
        shalong_baoming_num = OrderInfo.objects.filter(user_id=user_id, luyou='/activity/shalong',
                                                       pay_status='TRADE_SUCCESS').count()
        yue_baoming_num = OrderInfo.objects.filter(luyou='/activity/yuebao', user_id=user_id,
                                                   pay_status='TRADE_SUCCESS').count()
        tuijie_baoming_num = OrderInfo.objects.filter(luyou='/activity/tuijie', user_id=user_id,
                                                      pay_status='TRADE_SUCCESS').count()
        # 下载
        nadi_down_num = OrderInfo.objects.filter(luyou="/tudilist/nadi", user_id=user_id,
                                                 pay_status='TRADE_SUCCESS').count()
        gongdi_down_num = OrderInfo.objects.filter(luyou='/tudilist/gongdi', user_id=user_id,
                                                   pay_status='TRADE_SUCCESS').count()
        shoulou_down_num = OrderInfo.objects.filter(luyou='/tudilist/shoulou', user_id=user_id,
                                                    pay_status='TRADE_SUCCESS').count()
        loupan_down_num = OrderInfo.objects.filter(luyou='/tudilist/loupan', user_id=user_id,
                                                   pay_status='TRADE_SUCCESS').count()

        zhoubao_down_num = OrderInfo.objects.filter(luyou="/Investment/zhoubao", user_id=user_id,
                                                    pay_status='TRADE_SUCCESS').count()
        yuebao_down_num = OrderInfo.objects.filter(luyou="/Investment/yuebao", user_id=user_id,
                                                   pay_status='TRADE_SUCCESS').count()
        jibao_down_num = OrderInfo.objects.filter(luyou="/Investment/jibao", user_id=user_id,
                                                  pay_status='TRADE_SUCCESS').count()
        bannianbao_down_num = OrderInfo.objects.filter(luyou="/Investment/bannianbao", user_id=user_id,
                                                       pay_status='TRADE_SUCCESS').count()
        nianbao_down_num = OrderInfo.objects.filter(luyou="/Investment/nianbao", user_id=user_id,
                                                    pay_status='TRADE_SUCCESS').count()
        # 赞
        zan_num = Zan.objects.filter(user_id=user_id, zc=1).count()
        # 踩
        cai_num = Zan.objects.filter(user_id=user_id, zc=2).count()
        # 发送的邀请
        yaoqing_num = YaoQing.objects.filter(yaoqingren=user_id).count()
        # 收到的邀请
        yaoqinged_num = YaoQing.objects.filter(user_id=user_id).count()

        if info == 'userinfo1':
            project_collections = nitui_collection_num + paimai_collection_num + guapai_collection_num + zhuanrang_collection_num + zhaoshang_collection_num + xiancheng_collection_num
            project_receives = nitui_receive_num + paimai_receive_num + guapai_receive_num + zhuanrang_receive_num + zhaoshang_receive_num + xiancheng_receive_num
            activity_collections = shalong_collection_num + yuebao_collection_num + tuijie_collection_num
            pro_collections = nadi_collection_num + gongdi_collection_num + shoulou_collection_num + loupan_collection_num
            data_collections = zhoubao_collection_num + yue_collection_num + jibao_collection_num + bannianbao_collection_num + nianbao_collection_num
            data['111'] = project_receives
            data['112'] = yaoqing_num
            data['113'] = yaoqinged_num
            data[
                '114'] = nitui_contact_num + paimai_contact_num + guapai_contact_num + zhuanrang_contact_num + zhaoshang_contact_num + xiancheng_contact_num
            data[
                '115'] = paimai_contacted_num + zhuanrang_contacted_num + zhaoshang_contacted_num + xiancheng_contacted_num
            data['116'] = project_collections + activity_collections + pro_collections + data_collections
            data['117'] = fabu_num
            data['118'] = shalong_receive_num + yue_receive_num + tuijie_receive_num
            data['119'] = shalong_baoming_num + yue_baoming_num + tuijie_baoming_num
            data['1110'] = nadi_receive_num + gongdi_receive_num + shoulou_receive_num + loupan_receive_num
            data[
                '1111'] = zhoubao_receive_num + yuebao_receive_num + jibao_receive_num + bannianbao_receive_num + nianbao_receive_num
            data[
                '1112'] = nadi_down_num + gongdi_down_num + shoulou_down_num + loupan_down_num + zhoubao_down_num + yuebao_down_num + jibao_down_num + bannianbao_down_num + nianbao_down_num
            login_records = LoginRecord.objects.filter(user_id=user_id)
            # TODO：
            active_days = []
            for login_record in login_records:
                if login_record.create_on not in active_days:
                    timeArray = time.mktime(login_record.create_on.timetuple())
                    if timeArray > self.get_month_first_str():
                        if timeArray < self.get_month_last_str():
                            active_days.append(login_record.create_on)

            return Response({'msg': '获取成功', 'status': '1', 'data': data, 'active_days': len(active_days)})
        elif info == 'userinfo2':
            orders = OrderInfo.objects.filter(user_id=user_id, pay_status='TRADE_SUCCESS')
            if not orders:
                return Response({'msg': '无消费记录', 'status': '0'})
            day_data = 0
            weak_data = 0
            month_data = 0
            year_data = 0
            for order in orders:
                t = datetime.datetime(order.pay_time.year, order.pay_time.month, order.pay_time.day, 0, 0, 0)
                time_array = time.mktime(t.timetuple())
                if time_array == self.get_today_str():
                    day_data += order.order_mount
                if time_array > self.get_weak_first_str():
                    if time_array < self.get_weak_last_str():
                        weak_data += order.order_mount
                if time_array > self.get_month_first_str():
                    if time_array < self.get_month_last_str():
                        month_data += order.order_mount
                if time_array > self.get_year_first_str():
                    if time_array < self.get_year_last_str():
                        year_data += order.order_mount

            data = {'211': round(day_data, 2), '212': round(weak_data, 2), '213': round(month_data, 2),
                    '214': round(year_data, 2)}
            return Response({'msg': '获取成功', 'status': '1', 'data': data})
        elif info == 'userinfo3':
            nitui_yaoqing_num = YaoQing.objects.filter(user_id=user_id, luyou='/tudimessage/nitui').count()
            paimai_yaoqing_num = YaoQing.objects.filter(luyou='/tudimessage/paimai', user_id=user_id, ).count()
            guapai_yaoqing_num = YaoQing.objects.filter(luyou='/tudimessage/guapai', user_id=user_id, ).count()
            zhuanrang_yaoqing_num = YaoQing.objects.filter(luyou='/tudimessage/zhuanrang',
                                                           user_id=user_id, ).count()
            zhaoshang_yaoqing_num = YaoQing.objects.filter(luyou='/tudimessage/zhaoshang',
                                                           user_id=user_id, ).count()
            xiancheng_yaoqing_num = YaoQing.objects.filter(luyou='/tudimessage/xiancheng',
                                                           user_id=user_id, ).count()
            # 1
            data[
                '311'] = nitui_receive_num + paimai_receive_num + guapai_receive_num + zhuanrang_receive_num + zhaoshang_receive_num + xiancheng_receive_num
            data[
                '312'] = nitui_contact_num + paimai_contact_num + guapai_contact_num + zhuanrang_contact_num + zhaoshang_contact_num + xiancheng_contact_num
            data[
                '313'] = paimai_contacted_num + zhuanrang_contacted_num + zhaoshang_contacted_num + xiancheng_contacted_num
            data[
                '314'] = nitui_yaoqing_num + paimai_yaoqing_num + guapai_yaoqing_num + zhuanrang_yaoqing_num + zhaoshang_yaoqing_num + xiancheng_yaoqing_num
            data[
                '315'] = nitui_collection_num + paimai_collection_num + guapai_collection_num + zhuanrang_collection_num + zhaoshang_collection_num + xiancheng_collection_num
            data['316'] = zan_num
            data['317'] = cai_num
            # 2
            data['321'] = nitui_yaoqing_num
            data['322'] = nitui_receive_num
            data['323'] = nitui_contact_num
            data['324'] = nitui_collection_num
            # 3
            data['331'] = paimai_yaoqing_num
            data['332'] = paimai_receive_num
            data['333'] = paimai_contact_num
            data['334'] = paimai_contacted_num
            data['335'] = paimai_collection_num
            # 4
            data['341'] = zhuanrang_yaoqing_num
            data['342'] = zhuanrang_receive_num
            data['343'] = zhuanrang_contact_num
            data['344'] = zhuanrang_contacted_num
            data['345'] = zhuanrang_collection_num
            data['346'] = zan_num
            data['347'] = cai_num
            # 5
            data['351'] = guapai_yaoqing_num
            data['352'] = guapai_receive_num
            data['353'] = guapai_collection_num
            # 6
            data['361'] = zhaoshang_yaoqing_num
            data['362'] = zhaoshang_receive_num
            data['363'] = zhaoshang_contact_num
            data['364'] = zhaoshang_contacted_num
            data['365'] = zhaoshang_collection_num
            # 7
            data['371'] = xiancheng_yaoqing_num
            data['372'] = xiancheng_receive_num
            data['373'] = xiancheng_contact_num
            data['374'] = xiancheng_contacted_num
            data['375'] = xiancheng_collection_num
            return Response({'msg': '获取成功', 'status': '1', 'data': data})
        elif info == 'userinfo4':
            shalong_yaoqing_num = YaoQing.objects.filter(user_id=user_id, luyou='/activity/shalong').count()
            yue_yaoqing_num = YaoQing.objects.filter(luyou='/activity/yuebao', user_id=user_id, ).count()
            tuijie_yaoqing_num = YaoQing.objects.filter(luyou='/activity/tuijie', user_id=user_id, ).count()
            data['411'] = shalong_yaoqing_num + yue_yaoqing_num + tuijie_yaoqing_num
            data['412'] = shalong_receive_num + yue_receive_num + tuijie_receive_num
            data['413'] = shalong_baoming_num + yue_baoming_num + tuijie_baoming_num
            data['414'] = shalong_collection_num + yuebao_collection_num + tuijie_collection_num

            data['421'] = shalong_yaoqing_num
            data['422'] = shalong_receive_num
            data['423'] = shalong_baoming_num
            data['424'] = shalong_collection_num

            data['431'] = yue_yaoqing_num
            data['432'] = yue_receive_num
            data['433'] = yue_baoming_num
            data['434'] = yuebao_collection_num

            data['441'] = tuijie_yaoqing_num
            data['442'] = tuijie_receive_num
            data['443'] = tuijie_baoming_num
            data['444'] = tuijie_collection_num
            return Response({'msg': '获取成功', 'status': '1', 'data': data})
        elif info == 'userinfo5':
            nadi_yaoqing_num = YaoQing.objects.filter(luyou="/tudilist/nadi", user_id=user_id, ).count()
            gongdi_yaoqing_num = YaoQing.objects.filter(luyou='/tudilist/gongdi', user_id=user_id, ).count()
            shoulou_yaoqing_num = YaoQing.objects.filter(luyou='/tudilist/shoulou', user_id=user_id, ).count()
            loupan_yaoqing_num = YaoQing.objects.filter(luyou='/tudilist/loupan', user_id=user_id, ).count()
            data['511'] = nadi_yaoqing_num + gongdi_yaoqing_num + shoulou_yaoqing_num + loupan_yaoqing_num
            data['512'] = nadi_receive_num + gongdi_receive_num + shoulou_receive_num + loupan_receive_num
            data['513'] = nadi_down_num + gongdi_down_num + shoulou_down_num + loupan_down_num
            data['514'] = nadi_collection_num + gongdi_collection_num + shoulou_collection_num + loupan_collection_num

            data['521'] = nadi_yaoqing_num
            data['522'] = nadi_receive_num
            data['523'] = nadi_down_num
            data['524'] = nadi_collection_num

            data['531'] = gongdi_yaoqing_num
            data['532'] = gongdi_receive_num
            data['533'] = gongdi_down_num
            data['534'] = gongdi_collection_num

            data['541'] = shoulou_yaoqing_num
            data['542'] = shoulou_receive_num
            data['543'] = shoulou_down_num
            data['544'] = shoulou_collection_num

            data['551'] = loupan_yaoqing_num
            data['552'] = loupan_receive_num
            data['553'] = loupan_down_num
            data['554'] = loupan_collection_num
            return Response({'msg': '获取成功', 'status': '1', 'data': data})
        elif info == 'userinfo6':
            zhoubao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/zhoubao", user_id=user_id, ).count()
            yuebao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/yuebao", user_id=user_id, ).count()
            jibao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/jibao", user_id=user_id, ).count()
            bannianbao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/bannianbao", user_id=user_id, ).count()
            nianbao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/nianbao", user_id=user_id, ).count()
            data[
                '611'] = zhoubao_yaoqing_num + yuebao_yaoqing_num + jibao_yaoqing_num + bannianbao_yaoqing_num + nianbao_yaoqing_num
            data[
                '612'] = zhoubao_receive_num + yuebao_receive_num + jibao_receive_num + bannianbao_receive_num + nianbao_receive_num
            data['613'] = zhoubao_down_num + yuebao_down_num + jibao_down_num + bannianbao_down_num + nianbao_down_num
            data[
                '614'] = zhoubao_collection_num + yue_collection_num + jibao_collection_num + bannianbao_collection_num + nianbao_collection_num

            data['621'] = zhoubao_yaoqing_num
            data['622'] = zhoubao_receive_num
            data['623'] = zhoubao_down_num
            data['624'] = zhoubao_collection_num

            data['631'] = yuebao_yaoqing_num
            data['632'] = yuebao_receive_num
            data['633'] = yuebao_down_num
            data['634'] = yue_collection_num

            data['641'] = jibao_yaoqing_num
            data['642'] = jibao_receive_num
            data['643'] = jibao_down_num
            data['644'] = jibao_collection_num

            data['651'] = bannianbao_yaoqing_num
            data['652'] = bannianbao_receive_num
            data['653'] = bannianbao_down_num
            data['654'] = bannianbao_collection_num

            data['661'] = nianbao_yaoqing_num
            data['662'] = nianbao_receive_num
            data['663'] = nianbao_down_num
            data['664'] = nianbao_collection_num

            return Response({'msg': '获取成功', 'status': '1', 'data': data})
        elif info == 'userinfo8':
            fabu_num = ReleaseRecord.objects.filter(user_id=user_id, ).count()
            yaoqing_num = YaoQing.objects.filter(yaoqingren=user_id, ).count()
            records = ReleaseRecord.objects.filter(user_id=user_id)
            chakan_num = 0
            shoucang_num = 0
            fabu_zan_num = 0
            fabu_cai_num = 0
            for record in records:
                chakan_count = ReceivePeo.objects.filter(luyou=record.luyou, information_id=record.land_id).count()
                shoucang_count = Collection.objects.filter(luyou=record.luyou, information_id=record.land_id).count()
                fabu_zan_count = Zan.objects.filter(luyou=record.luyou, land_id=record.land_id, zc=1).count()
                fabu_cai_count = Zan.objects.filter(luyou=record.luyou, land_id=record.land_id, zc=2).count()
                chakan_num += chakan_count
                shoucang_num += shoucang_count
                fabu_zan_num += fabu_zan_count
                fabu_cai_num += fabu_cai_count

            lianxi_num = Contact.objects.filter(contacted_id=user_id).count()

            data['811'] = fabu_num
            data['812'] = yaoqing_num
            data['813'] = chakan_num
            data[
                '814'] = nitui_contact_num + paimai_contact_num + guapai_contact_num + zhuanrang_contact_num + zhaoshang_contact_num + xiancheng_contact_num
            data['815'] = lianxi_num
            data['816'] = shoucang_num
            objs = ReleaseRecord.objects.filter(user_id=user_id, luyou__in=['/tudimessage/paimai', '/tudimessage/nitui',
                                                                            '/tudimessage/guapai',
                                                                            '/tudimessage/zhuanrang',
                                                                            '/tudimessage/zhaoshang',
                                                                            '/tudimessage/xiancheng'])
            if not objs:
                return Response({'msg': '无发布记录', 'status': '1', 'data': data, })
            seria = ReleaseRecordListSerializers(objs, many=True, context={'user_id': user_id})
            return Response({'msg': '获取成功', 'status': '1', 'data': data, 'record_data': seria.data})
        else:
            return Response({'msg': 'erro', 'status': '0', })


# TODO：个人中心表格
class SelfTableView(LoginRequiredMixin, APIView):

    def get(self, request):
        user_id = request.GET.get("user_id")
        if not user_id:
            return Response({'msg': '没传userid', 'status': '0', })
        info = request.GET.get('info', '114')
        # 拟推
        if info == '114' or info == '312' or info == '814':
            land_luyou = ['/tudimessage/nitui', '/tudimessage/paimai', '/tudimessage/guapai', '/tudimessage/xiancheng']
            obj_land = Contact.objects.filter(user_id=user_id, luyou__in=land_luyou)
            seria_land = SelfLandInfoContactTableSerializer(obj_land, many=True)
            obj_trans = Contact.objects.filter(user_id=user_id, luyou='/tudimessage/zhuanrang')
            seria_trans = SelfTransInfoContactTableSerializer(obj_trans, many=True, context={'user_id': user_id})
            obj_attract = Contact.objects.filter(user_id=user_id, luyou='/tudimessage/zhaoshang')
            seria_attract = SelfAttractContactTableSerializer(obj_attract, many=True)
            data = seria_land.data + seria_trans.data + seria_attract.data
            return Response({'msg': '获取成功', 'status': '1', 'data': data})
        if info == '115' or info == '313' or info == '815':
            land_luyou = ['/tudimessage/nitui', '/tudimessage/paimai', '/tudimessage/guapai', '/tudimessage/xiancheng']
            obj_land = Contact.objects.filter(contacted_id=user_id, luyou__in=land_luyou)
            seria_land = SelfLandInfoContactedTableSerializer(obj_land, many=True)
            obj_trans = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/zhuanrang')
            seria_trans = SelfTransInfoContactedTableSerializer(obj_trans, many=True, context={'user_id': user_id})
            obj_attract = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/zhaoshang')
            seria_attract = SelfAttractContactedTableSerializer(obj_attract, many=True)
            data = seria_land.data + seria_trans.data + seria_attract.data
            return Response({'msg': '获取成功', 'status': '1', 'data': data})
        elif info == '321':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/tudimessage/nitui').order_by('-id')
            seria = SelfLandInfoYaoqingTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '322':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/tudimessage/nitui').order_by('-id')
            seria = SelfLandInfoReceiveTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '323':
            obj = Contact.objects.filter(user_id=user_id, luyou='/tudimessage/nitui').order_by('-id')
            seria = SelfLandInfoContactTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '324':
            obj = Collection.objects.filter(user_id=user_id, luyou='/tudimessage/nitui').order_by('-id')
            seria = SelfLandInfoCollectionTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 拍卖
        elif info == '331':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/tudimessage/paimai').order_by('-id')
            seria = SelfLandInfoYaoqingTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '332':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/tudimessage/paimai').order_by('-id')
            seria = SelfLandInfoReceiveTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '333':
            obj = Contact.objects.filter(user_id=user_id, luyou='/tudimessage/paimai').order_by('-id')
            seria = SelfLandInfoContactTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '334':
            obj = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/paimai')
            seria = SelfLandInfoContactedTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '335':
            obj = Collection.objects.filter(user_id=user_id, luyou='/tudimessage/paimai').order_by('-id')
            seria = SelfLandInfoCollectionTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 转让
        elif info == '341':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/tudimessage/zhuanrang').order_by('-id')
            seria = SelfTransInfoYaoqingSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '342':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/tudimessage/zhuanrang').order_by('-id')
            seria = SelfTransInfoReceiveSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '343':
            obj = Contact.objects.filter(user_id=user_id, luyou='/tudimessage/zhuanrang').order_by('-id')
            seria = SelfTransInfoContactTableSerializer(obj, many=True, context={'user_id': user_id})
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '344':
            obj = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/zhuanrang')
            seria = SelfTransInfoContactedTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '345':
            obj = Collection.objects.filter(user_id=user_id, luyou='/tudimessage/zhuanrang').order_by('-id')
            seria = SelfTransInfoCollectionSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '346':
            obj = Zan.objects.filter(user_id=user_id, luyou='/tudimessage/zhuanrang', zc=1).order_by('-id')
            seria = SelfTransInfoZanSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '347':
            obj = Zan.objects.filter(user_id=user_id, luyou='/tudimessage/zhuanrang', zc=2).order_by('-id')
            seria = SelfTransInfoZanSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '351':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/tudimessage/guapai').order_by('-id')
            seria = SelfLandInfoYaoqingTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '352':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/tudimessage/guapai').order_by('-id')
            seria = SelfLandInfoGuapaiReceiveTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '353':
            obj = Collection.objects.filter(user_id=user_id, luyou='/tudimessage/guapai').order_by('-id')
            seria = SelfLandInfoCollectionTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '361':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/tudimessage/zhaoshang').order_by('-id')
            seria = SelfAttractYaoqingSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '362':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/tudimessage/zhaoshang').order_by('-id')
            seria = SelfAttractInfoReceiveSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '363':
            obj = Contact.objects.filter(user_id=user_id, luyou='/tudimessage/zhaoshang').order_by('-id')
            seria = SelfAttractContactTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '364':
            obj = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/zhaoshang')
            seria = SelfAttractContactedTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '365':
            obj = Collection.objects.filter(user_id=user_id, luyou='/tudimessage/zhaoshang').order_by('-id')
            seria = SelfAttractInfoCollectionSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 县城
        elif info == '371':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/tudimessage/xiancheng').order_by('-id')
            seria = SelfLandInfoYaoqingTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '372':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/tudimessage/xiancheng').order_by('-id')
            seria = SelfLandInfoReceiveTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '373':
            obj = Contact.objects.filter(user_id=user_id, luyou='/tudimessage/xiancheng').order_by('-id')
            seria = SelfLandInfoContactTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '374':
            obj = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/xiancheng')
            seria = SelfLandInfoContactedTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '375':
            obj = Collection.objects.filter(user_id=user_id, luyou='/tudimessage/xiancheng').order_by('-id')
            seria = SelfLandInfoCollectionTableSerializer(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '413':
            obj = OrderInfo.objects.filter(user_id=user_id,
                                           luyou__in=['/activity/shalong', '/activity/yuebao', '/activity/tuijie',
                                                      '/activity/kuanian'], pay_status='TRADE_SUCCESS').order_by('-id')
            seria = ActivitySingUpSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 活动邀请
        elif info == '421':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/activity/shalong')
            seria = ActivityYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '431':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/activity/yuebao')
            seria = ActivityYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '441':
            obj = YaoQing.objects.filter(user_id=user_id, luyou='/activity/tuijie')
            seria = ActivityYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 活动查看
        elif info == '422':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/activity/shalong').order_by('-id')
            seria = ActivityReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '432':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/activity/yuebao').order_by('-id')
            seria = ActivityReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '442':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou='/activity/tuijie').order_by('-id')
            seria = ActivityReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 活动报名
        elif info == '423':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou='/activity/shalong').order_by('-id')
            seria = ActivitySingUpSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '433':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou='/activity/yuebao').order_by('-id')
            seria = ActivitySingUpSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '443':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou='/activity/tuijie').order_by('-id')
            seria = ActivitySingUpSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 活动收藏
        elif info == '424':
            obj = Collection.objects.filter(user_id=user_id, luyou='/activity/shalong').order_by('-id')
            seria = ActivityCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '434':
            obj = Collection.objects.filter(user_id=user_id, luyou='/activity/yuebao').order_by('-id')
            seria = ActivityCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '444':
            obj = Collection.objects.filter(user_id=user_id, luyou='/activity/tuijie').order_by('-id')
            seria = ActivityCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '454':
            obj = Collection.objects.filter(user_id=user_id, luyou='/activity/kuanian').order_by('-id')
            seria = ActivityCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '513':
            obj = OrderInfo.objects.filter(user_id=user_id,
                                           luyou__in=["/tudilist/nadi", "/tudilist/gongdi", "/tudilist/shoulou",
                                                      "/tudilist/loupan"],
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = PropertyListDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 榜单接收
        elif info == '521':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/tudilist/nadi").order_by('-id')
            seria = PropertyListYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '531':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/tudilist/gongdi").order_by('-id')
            seria = PropertyListYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '541':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/tudilist/shoulou").order_by('-id')
            seria = PropertyListYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '551':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/tudilist/loupan").order_by('-id')
            seria = PropertyListYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 榜单查看
        elif info == '522':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/tudilist/nadi").order_by('-id')
            seria = PropertyListReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '532':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/tudilist/gongdi").order_by('-id')
            seria = PropertyListReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '542':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/tudilist/shoulou").order_by('-id')
            seria = PropertyListReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '552':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/tudilist/loupan").order_by('-id')
            seria = PropertyListReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 榜单下载
        elif info == '523':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/tudilist/nadi",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = PropertyListDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '533':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/tudilist/gongdi",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = PropertyListDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '543':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/tudilist/loupan",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = PropertyListDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '553':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/tudilist/shoulou",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = PropertyListDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 榜单收藏
        elif info == '524':
            obj = Collection.objects.filter(user_id=user_id, luyou="/tudilist/nadi").order_by('-id')
            seria = PropertyListCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '534':
            obj = Collection.objects.filter(user_id=user_id, luyou="/tudilist/gongdi").order_by('-id')
            seria = PropertyListCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '544':
            obj = Collection.objects.filter(user_id=user_id, luyou="/tudilist/shoulou").order_by('-id')
            seria = PropertyListCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '554':
            obj = Collection.objects.filter(user_id=user_id, luyou="/tudilist/loupan").order_by('-id')
            seria = PropertyListCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '613':
            obj = OrderInfo.objects.filter(user_id=user_id,
                                           luyou__in=["/Investment/zhoubao", "/Investment/yuebao", "/Investment/jibao",
                                                      "/Investment/bannianbao", "/Investment/nianbao"],
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = InvestmentDataDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 数据接收
        elif info == '621':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/Investment/zhoubao").order_by('-id')
            seria = InvestmentDataYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '631':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/Investment/yuebao").order_by('-id')
            seria = InvestmentDataYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '641':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/Investment/jibao").order_by('-id')
            seria = InvestmentDataYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '651':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/Investment/banjianbao").order_by('-id')
            seria = InvestmentDataYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '661':
            obj = YaoQing.objects.filter(user_id=user_id, luyou="/Investment/nianbao").order_by('-id')
            seria = InvestmentDataYaoqingSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 数据查看
        elif info == '622':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/Investment/zhoubao").order_by('-id')
            seria = InvestmentDataReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '632':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/Investment/yuebao").order_by('-id')
            seria = InvestmentDataReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '642':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/Investment/jibao").order_by('-id')
            seria = InvestmentDataReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '652':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/Investment/banjianbao").order_by('-id')
            seria = InvestmentDataReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '662':
            obj = ReceivePeo.objects.filter(user_id=user_id, luyou="/Investment/nianbao").order_by('-id')
            seria = InvestmentDataReceiveSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 数据下载
        elif info == '623':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/Investment/zhoubao",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = InvestmentDataDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '623':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/Investment/yuebao",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = InvestmentDataDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '623':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/Investment/jibao",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = InvestmentDataDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '623':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/Investment/banjianbao",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = InvestmentDataDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '623':
            obj = OrderInfo.objects.filter(user_id=user_id, luyou="/Investment/nianbao",
                                           pay_status='TRADE_SUCCESS').order_by('-id')
            seria = InvestmentDataDownSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        # 数据收藏
        elif info == '624':
            obj = Collection.objects.filter(user_id=user_id, luyou="/Investment/zhoubao").order_by('-id')
            seria = InvestmentDataCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '634':
            obj = Collection.objects.filter(user_id=user_id, luyou="/Investment/yuebao").order_by('-id')
            seria = InvestmentDataCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '644':
            obj = Collection.objects.filter(user_id=user_id, luyou="/Investment/jibao").order_by('-id')
            seria = InvestmentDataCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '654':
            obj = Collection.objects.filter(user_id=user_id, luyou="/Investment/banjianbao").order_by('-id')
            seria = InvestmentDataCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        elif info == '664':
            obj = Collection.objects.filter(user_id=user_id, luyou="/Investment/jianbao").order_by('-id')
            seria = InvestmentDataCollectionSerializers(obj, many=True)
            return Response({'msg': '获取成功', 'status': '1', 'data': seria.data})
        else:
            return Response({'msg': '获取失败', 'status': '0'})
