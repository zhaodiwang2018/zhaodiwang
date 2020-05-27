from rest_framework.views import APIView, Response
from apps.land.serializers import *
from apps.user.models import *
from apps.land.forms import *
from apps.utils.mixin_utils import LoginRequiredMixin


# TODO：审核公告
class AuditLandView(LoginRequiredMixin, APIView):
    """
    get:获取信息
    post：审核
    """

    def get(self, request):
        land_id = request.GET.get("land_id", 91)
        land_info = LandInfo.objects.filter(id=land_id)
        seria = ClientLandSerializers(land_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1'})

    def post(self, request):
        land_id = request.data.get("land_id", 91)
        land = LandInfo.objects.filter(id=land_id).first()
        luyou = ['/tudimessage/nitui', '/tudimessage/paimai', '/tudimessage/guapai', '/tudimessage/xiancheng']
        user_record = ReleaseRecord.objects.filter(land_id=land_id, luyou__in=luyou).first()
        if user_record:
            user_id = user_record.user_id
        else:
            user_id = 0
        opinion = request.data.get('opinion')
        result = request.data.get('result')
        if result == 0:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='land').first()
            if audit:
                audit.opinion = opinion
                audit.save()
            else:
                AuditOpinion.objects.create(opinion=opinion, user_id=user_id, land_id=land_id, source='land')
            land.audit_state = 1
            land.save()
            return Response({'msg': '成功', 'status': '1'})
        elif result == 1:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='land').first()
            users = Users.objects.filter(city__contains=land.city)
            if audit:
                audit.opinion = '审核通过'
                audit.save()
                # 审核通过发送邀请
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=land.id, luyou=user_record.luyou,
                                                  yaoqingren=user_record.user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=land.id, luyou=user_record.luyou,
                                               yaoqingren=user_record.user_id)
            else:

                AuditOpinion.objects.create(opinion='审核通过', user_id=user_id, land_id=land_id, source='land')
                # 审核通过发送邀请
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=land.id, luyou=user_record.luyou,
                                                  yaoqingren=user_record.user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=land.id, luyou=user_record.luyou,
                                               yaoqingren=user_record.user_id)  # land = LandInfo.objects.filter(id=land_id).first()
            land.audit_state = 2
            land.save()
            # TODO: 群发短信
            # mobile_list = []
            # for user in users:
            #     mobile_list.append(user.mobile)
            # mobiles = ','.join(str(n) for n in mobile_list)
            # print(mobiles)
            # TODO: 存日历需要的数据
            if land.land_type in ['1', '3']:
                date_day = Calendar.objects.filter(c_date=land.listed_date).first()
                if date_day:
                    h_list = eval(date_day.big_list)
                    s_list = []
                    land_id_list = []
                    for city_s in h_list:
                        for c, o in city_s.items():
                            s_list.append(c)
                            for s in o:
                                land_id_list.append(s['land_id'])
                    print(land_id_list)
                    print(type(land_id))
                    # TODO: 判断id
                    if int(land_id) not in land_id_list:
                        flag = False
                        for s_l in s_list:
                            if land.city in s_l:
                                for ci_i in h_list:
                                    l_list = ci_i.get(land.city)
                                    if l_list:
                                        l_list.append({'title': land.title, 'land_type': land.land_type, 'land_id': land.id,
                                                       'img': land.img,
                                                       'serial_number': land.serial_number})
                                        date_day.big_list = str(h_list)
                                        date_day.save()
                                    else:
                                        pass
                                flag = True
                        if flag is False:
                            # print(land.city)
                            info_list = []
                            info_obj = {'title': land.title, 'land_type': land.land_type, 'land_id': land.id,
                                        'img': land.img,
                                        'serial_number': land.serial_number}
                            info_list.append(info_obj)
                            info_dic = {land.city: info_list}
                            # print(info_dic)
                            h_list.append(info_dic)
                            date_day.big_list = str(h_list)
                            date_day.save()
                else:

                    big_list = []
                    info_list = []
                    info_obj = {'title': land.title, 'land_type': land.land_type, 'land_id': land.id, 'img': land.img,
                                'serial_number': land.serial_number}
                    info_list.append(info_obj)
                    city_obj = {land.city: info_list}
                    big_list.append(city_obj)
                    Calendar.objects.create(c_date=land.listed_date, big_list=str(big_list))
                transfer_date_day = Calendar.objects.filter(c_date=land.transfer_date).first()
                if transfer_date_day:
                    transfer_h_list = eval(transfer_date_day.big_list)
                    transfer_s_list = []
                    transfer_land_id_list = []
                    for transfer_city_s in transfer_h_list:
                        for transfer_c, transfer_o in transfer_city_s.items():
                            transfer_s_list.append(transfer_c)
                            for s in transfer_o:
                                transfer_land_id_list.append(s['land_id'])
                    # TODO: 判断id
                    if int(land_id) not in transfer_land_id_list:
                        flag = False
                        for transfer_s_l in transfer_s_list:
                            if land.city in transfer_s_l:
                                for transfer_ci_i in transfer_h_list:
                                    transfer_l_list = transfer_ci_i.get(land.city)
                                    if transfer_l_list:
                                        transfer_l_list.append(
                                            {'title': land.title, 'land_type': land.land_type, 'land_id': land.id,
                                             'img': land.img,
                                             'serial_number': land.serial_number})
                                        transfer_date_day.big_list = str(transfer_h_list)
                                        transfer_date_day.save()
                                    else:
                                        pass
                                flag = True
                        if flag is False:
                            transfer_info_list = []
                            transfer_info_obj = {'title': land.title, 'land_type': land.land_type, 'land_id': land.id,
                                                 'img': land.img,
                                                 'serial_number': land.serial_number}
                            transfer_info_list.append(transfer_info_obj)
                            transfer_info_dic = {land.city: transfer_info_list}
                            transfer_h_list.append(transfer_info_dic)
                            transfer_date_day.big_list = str(transfer_h_list)
                            transfer_date_day.save()
                else:

                    transfer_big_list = []
                    transfer_info_list = []
                    transfer_info_obj = {'title': land.title, 'land_type': land.land_type, 'land_id': land.id,
                                         'img': land.img,
                                         'serial_number': land.serial_number}
                    transfer_info_list.append(transfer_info_obj)
                    transfer_city_obj = {land.city: transfer_info_list}
                    transfer_big_list.append(transfer_city_obj)
                    Calendar.objects.create(c_date=land.transfer_date, big_list=str(transfer_big_list))
            return Response({'msg': '成功', 'status': '1'})
        return Response({'msg': '错误信息', 'status': '1'})


# TODO：审核转让
class AuditTransView(LoginRequiredMixin, APIView):
    """
    get:获取信息
    post：审核
    """

    def get(self, request):
        land_id = request.GET.get("land_id", 91)
        land_info = TransInfo.objects.filter(id=land_id)
        seria = ClientTransSerializers(land_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1'})

    def post(self, request):
        land_id = request.data.get("land_id", 91)
        trans = TransInfo.objects.filter(id=land_id).first()
        user_record = ReleaseRecord.objects.filter(land_id=land_id, luyou='/tudimessage/zhuanrang').first()
        if user_record:
            user_id = user_record.user_id
        else:
            user_id = 0
        opinion = request.data.get('opinion', 'hahaha')
        result = request.data.get('result', 0)
        if result == 0:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='trans').first()
            if audit:
                audit.opinion = opinion
                audit.save()
            else:
                AuditOpinion.objects.create(opinion=opinion, user_id=user_id, land_id=land_id, source='trans')

            trans.audit_state = 1
            trans.save()
            return Response({'msg': '成功', 'status': '1'})
        elif result == 1:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='trans').first()
            if audit:
                audit.opinion = '审核通过'
                audit.save()
                # 审核通过发送邀请
                users = Users.objects.filter(city__contains=trans.city)
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=trans.id, luyou='/tudimessage/zhuanrang',
                                                  yaoqingren=user_record.user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=trans.id, luyou='/tudimessage/zhuanrang',
                                               yaoqingren=user_record.user_id)
            else:

                AuditOpinion.objects.create(opinion='审核通过', user_id=user_id, land_id=land_id, source='trans')
                # 审核通过发送邀请
                users = Users.objects.filter(city__contains=trans.city)
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=trans.id, luyou='/tudimessage/zhuanrang',
                                                  yaoqingren=user_record.user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=trans.id, luyou='/tudimessage/zhuanrang',
                                               yaoqingren=user_record.user_id)  # trans = TransInfo.objects.filter(id=land_id).first()
            trans.audit_state = 2
            trans.save()
            return Response({'msg': '成功', 'status': '1'})
        return Response({'msg': '错误信息', 'status': '1'})


# TODO：审核招商
class AuditAttractView(LoginRequiredMixin, APIView):
    """
    get:获取信息
    post：审核
    """

    def get(self, request):
        land_id = request.GET.get("land_id", 10)
        land_info = AttractInfo.objects.filter(id=land_id)
        seria = ClientAttractSerializers(land_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1'})

    def post(self, request):
        land_id = request.data.get("land_id", 91)
        attract = AttractInfo.objects.filter(id=land_id).first()

        user_record = ReleaseRecord.objects.filter(land_id=land_id, luyou='/tudimessage/zhaoshang').first()
        if user_record:
            user_id = user_record.user_id
        else:
            user_id = 0
        opinion = request.data.get('opinion', 'hahaha')
        result = request.data.get('result', 0)
        if result == 0:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='attract').first()
            if audit:
                audit.opinion = opinion
                audit.save()
            else:
                AuditOpinion.objects.create(opinion=opinion, user_id=user_id, land_id=land_id, source='attract')
            attract.audit_state = 1
            attract.save()
            return Response({'msg': '成功', 'status': '1'})
        elif result == 1:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='attract').first()
            if audit:
                audit.opinion = '审核通过'
                audit.save()
                # 审核通过发送邀请
                users = Users.objects.filter(city__contains=attract.city)
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=attract.id, luyou='/tudimessage/zhaoshang',
                                                  yaoqingren=user_record.user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=attract.id, luyou='/tudimessage/zhaoshang',
                                               yaoqingren=user_record.user_id)
            else:

                AuditOpinion.objects.create(opinion='审核通过', user_id=user_id, land_id=land_id, source='attract')
                # 审核通过发送邀请
                users = Users.objects.filter(city__contains=attract.city)  # __contains 筛选出包括的城市
                for user in users:

                    if not YaoQing.objects.filter(user_id=user.id, land_id=attract.id, luyou='/tudimessage/zhaoshang',
                                                  yaoqingren=user_record.user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=attract.id, luyou='/tudimessage/zhaoshang',
                                               yaoqingren=user_record.user_id)
            # attract = AttractInfo.objects.filter(id=land_id).first()
            attract.audit_state = 2
            attract.save()
            return Response({'msg': '成功', 'status': '1'})
        return Response({'msg': '错误信息', 'status': '1'})


# TODO：审核活动
class AuditActivityView(LoginRequiredMixin, APIView):
    """
    get:获取信息
    post：审核
    """

    def get(self, request):
        land_id = request.GET.get("land_id", 10)
        land_info = Activity.objects.filter(id=land_id)
        seria = ClientActivitySerializers(land_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1'})

    def post(self, request):
        land_id = request.data.get("land_id", 91)
        activity = Activity.objects.filter(id=land_id).first()
        luyou = ['/activity/shalong', '/activity/yuebao', '/activity/tuijie']
        user_record = ReleaseRecord.objects.filter(land_id=land_id, luyou__in=luyou).first()
        if user_record:
            user_id = user_record.user_id
        else:
            user_id = 0
        opinion = request.data.get('opinion', 'hahaha')
        result = request.data.get('result', 0)
        if result == 0:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='activity').first()
            if audit:
                audit.opinion = opinion
                audit.save()
            else:
                AuditOpinion.objects.create(opinion=opinion, user_id=user_id, land_id=land_id, source='activity')
            activity.audit_state = 1
            activity.save()
            return Response({'msg': '成功', 'status': '1'})
        elif result == 1:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='activity').first()
            if audit:
                audit.opinion = '审核通过'
                audit.save()
                # 审核通过发送邀请

                users = Users.objects.all()
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=activity.id, luyou=user_record.luyou,
                                                  yaoqingren=user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=activity.id, luyou=user_record.luyou,
                                               yaoqingren=user_id)
                print('发送邀请成功')
            else:

                AuditOpinion.objects.create(opinion='审核通过', user_id=user_id, land_id=land_id, source='activity')
                # 审核通过发送邀请

                users = Users.objects.all()
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=activity.id, luyou=user_record.luyou,
                                                  yaoqingren=user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=activity.id, luyou=user_record.luyou,
                                               yaoqingren=user_id)
                print('发送邀请成功')
            # activity = Activity.objects.filter(id=land_id).first()
            activity.audit_state = 2
            activity.save()
            return Response({'msg': '成功', 'status': '1'})
        return Response({'msg': '错误信息', 'status': '1'})


# TODO：审核数据
class AuditInvestmentView(LoginRequiredMixin, APIView):
    """
    get:获取信息
    post：审核
    """

    def get(self, request):
        land_id = request.GET.get("land_id", 10)
        land_info = InvestmentData.objects.filter(id=land_id)
        seria = ClientInvestmentDataSerializers(land_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1'})

    def post(self, request):
        land_id = request.data.get("land_id", 91)
        inv = InvestmentData.objects.filter(id=land_id).first()
        luyou = ['/Investment/zhoubao', '/Investment/yuebao', '/Investment/jibao', '/Investment/bannianbao',
                 '/Investment/nianbao']
        user_record = ReleaseRecord.objects.filter(land_id=land_id, luyou__in=luyou).first()
        if user_record:
            user_id = user_record.user_id
        else:
            user_id = 0
        opinion = request.data.get('opinion', 'hahaha')
        result = request.data.get('result', 0)
        if result == 0:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='inv').first()
            if audit:
                audit.opinion = opinion
                audit.save()
            else:
                AuditOpinion.objects.create(opinion=opinion, user_id=user_id, land_id=land_id, source='inv')
            inv.audit_state = 1
            inv.save()
            return Response({'msg': '成功', 'status': '1'})
        elif result == 1:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='inv').first()
            if audit:
                audit.opinion = '审核通过'
                audit.save()
                # 审核通过发送邀请

                users = Users.objects.all()
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=inv.id, luyou=user_record.luyou,
                                                  yaoqingren=user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=inv.id, luyou=user_record.luyou,
                                               yaoqingren=user_id)
                print('发送邀请成功')
            else:

                AuditOpinion.objects.create(opinion='审核通过', user_id=user_id, land_id=land_id, source='inv')
                # 审核通过发送邀请

                users = Users.objects.all()
                for user in users:
                    if not YaoQing.objects.filter(user_id=user.id, land_id=inv.id, luyou=user_record.luyou,
                                                  yaoqingren=user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=inv.id, luyou=user_record.luyou,
                                               yaoqingren=user_id)
                    print('发送邀请成功')
            # activity = PropertyList.objects.filter(id=land_id).first()
            inv.audit_state = 2
            inv.save()
            return Response({'msg': '成功', 'status': '1'})
        return Response({'msg': '错误信息', 'status': '1'})


# TODO：审核榜单
class AuditPopListView(LoginRequiredMixin, APIView):
    """
    get:获取信息
    post：审核
    """

    def get(self, request):
        land_id = request.GET.get("land_id", 10)
        land_info = PropertyList.objects.filter(id=land_id)
        seria = ClientPopListSerializers(land_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1'})

    def post(self, request):
        land_id = request.data.get("land_id", 91)
        poplist = PropertyList.objects.filter(id=land_id).first()
        luyou = ['/tudilist/nadi', '/tudilist/gongdi', '/tudilist/shoulou', '/tudilist/loupan']
        user_record = ReleaseRecord.objects.filter(land_id=land_id, luyou__in=luyou).first()
        if user_record:
            user_id = user_record.user_id
        else:
            user_id = 0
        opinion = request.data.get('opinion', 'hahaha')
        result = request.data.get('result', 0)
        if result == 0:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='poplist').first()
            if audit:
                audit.opinion = opinion
                audit.save()
            else:
                AuditOpinion.objects.create(opinion=opinion, user_id=user_id, land_id=land_id, source='poplist')
            poplist.audit_state = 1
            poplist.save()
            return Response({'msg': '成功', 'status': '1'})
        elif result == 1:
            audit = AuditOpinion.objects.filter(user_id=user_id, land_id=land_id, source='poplist').first()
            if audit:
                audit.opinion = '审核通过'
                audit.save()
                # 审核通过发送邀请

                users = Users.objects.all()
                for user in users:
                    if not YaoQing.objects.create(user_id=user.id, land_id=poplist.id, luyou=user_record.luyou,
                                                  yaoqingren=user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=poplist.id, luyou=user_record.luyou,
                                               yaoqingren=user_id)
                print('发送邀请成功')
            else:

                AuditOpinion.objects.create(opinion='审核通过', user_id=user_id, land_id=land_id, source='poplist')
                # 审核通过发送邀请

                users = Users.objects.all()
                for user in users:
                    if not YaoQing.objects.create(user_id=user.id, land_id=poplist.id, luyou=user_record.luyou,
                                                  yaoqingren=user_id):
                        YaoQing.objects.create(user_id=user.id, land_id=poplist.id, luyou=user_record.luyou,
                                               yaoqingren=user_id)
                print('发送邀请成功')
            # activity = PropertyList.objects.filter(id=land_id).first()
            poplist.audit_state = 2
            poplist.save()
            return Response({'msg': '成功', 'status': '1'})
        return Response({'msg': '错误信息', 'status': '1'})
