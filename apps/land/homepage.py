from rest_framework.views import APIView, Response
from apps.land.serializers import *
from apps.land.forms import *
from apps.user.models import *
from apps.user.smsnotice import *
from apps.utils.parsing import Parsing
import operator
import datetime
import time
from apps.utils.mixin_utils import LoginRequiredMixin

import re


# Create your views here.
class A(APIView):
    def get(self, request):
        users = Users.objects.filter(id__lte=76)
        company_list = []
        for user in users:
            if user.company:
                if len(user.company) > 1:
                    company_list.append(user.company)
        num_company = []
        for u_s in users:
            if u_s.company:
                if len(u_s.company) > 1:
                    n_m = {'company': u_s.company, 'num': company_list.count(u_s.company)}
                    num_company.append(n_m)
        ignored_keys = ["num"]
        filtered = {tuple((k, d[k]) for k in sorted(d) if k not in ignored_keys): d for d in num_company}
        dst_lst = list(filtered.values())
        data_list = sorted(dst_lst, key=operator.itemgetter('num'), reverse=True)

        return Response({'msg': '获取成功', 'status': '1', 'data': data_list, 'da': len(company_list)})

# TODO：首页
class HomePageView(APIView):

    def get(self, request):
        home_list = []
        nitui = LandInfo.objects.filter(land_type='2', audit_state=2)
        if not nitui:
            return Response({'data': home_list, 'status': '1'})
        seria_nitui = LandSerializers(nitui, many=True)
        home_list.append(seria_nitui.data[-1])
        paimai = LandInfo.objects.filter(land_type='3', audit_state=2)
        if not paimai:
            return Response({'data': home_list, 'status': '1'})
        seria_paimai = LandSerializers(paimai, many=True)
        home_list.append(seria_paimai.data[-1])
        zhuanrang = TransInfo.objects.filter(audit_state=2)
        if not zhuanrang:
            return Response({'data': home_list, 'status': '1'})
        seria_zhuanrang = TransSerializers(zhuanrang, many=True)
        home_list.append(seria_zhuanrang.data[-1])
        guapai = LandInfo.objects.filter(land_type='1',audit_state=2)
        if not guapai:
            return Response({'data': home_list, 'status': '1'})
        seria_guapai = LandSerializers(guapai, many=True)
        home_list.append(seria_guapai.data[-1])
        return Response({'data': home_list, 'status': '1'})


# TODO：榜单
class HotTop(LoginRequiredMixin, APIView):
    def get_days(self):
        a = datetime.datetime.now()
        b = datetime.timedelta(days=30)
        c = a - b
        return c

    def get_receive_top(self):
        hot_data = []
        lands = LandInfo.objects.filter(create_on__gte=self.get_days(), create_on__lte=datetime.datetime.now(), audit_state=2)
        trans = TransInfo.objects.filter(create_on__gte=self.get_days(), create_on__lte=datetime.datetime.now(), audit_state=2)
        attracts = AttractInfo.objects.filter(create_on__gte=self.get_days(), create_on__lte=datetime.datetime.now(), audit_state=2)
        for land in lands:
            hot_dic_land = {}
            luyou = ['/tudimessage/nitui', '/tudimessage/paimai', '/tudimessage/guapai', '/tudimessage/xiancheng', ]
            land_receives = ReceivePeo.objects.filter(information_id=land.id, luyou__in=luyou)
            if land_receives:
                for land_receive in land_receives:
                    record = ReleaseRecord.objects.filter(land_id=land.id, luyou__in=luyou).first()
                    if record:
                        user = Users.objects.filter(id=record.user_id).first()
                        if user:
                            if land_receive.luyou == '/tudimessage/nitui':
                                l_luyou = '拟推预告'
                            elif land_receive.luyou == '/tudimessage/paimai':
                                l_luyou = '拍卖公告'
                            elif land_receive.luyou == '/tudimessage/guapai':
                                l_luyou = '挂牌公告'
                            elif land_receive.luyou == '/tudimessage/xiancheng':
                                l_luyou = '县城土地'
                            else:
                                l_luyou = 'a'
                            hot_dic_land['id'] = land_receive.information_id
                            hot_dic_land['title'] = land.title
                            hot_dic_land['luyou'] = land_receive.luyou
                            hot_dic_land['leibie'] = l_luyou

                            hot_dic_land['user'] = user.username
                            hot_dic_land['land_receive'] = land_receives.count()
                if hot_dic_land:
                    hot_data.append(hot_dic_land)
        for tran in trans:
            hot_dic_tran = {}
            luyou = '/tudimessage/zhuanrang'
            trans_receives = ReceivePeo.objects.filter(information_id=tran.id, luyou=luyou)
            if trans_receives:
                for trans_receive in trans_receives:
                    record = ReleaseRecord.objects.filter(land_id=tran.id, luyou=luyou).first()
                    if record:
                        user = Users.objects.filter(id=record.user_id).first()
                        if user:
                            hot_dic_tran['id'] = trans_receive.information_id
                            hot_dic_tran['title'] = tran.title
                            hot_dic_tran['luyou'] = trans_receive.luyou
                            hot_dic_tran['leibie'] = '转让信息'
                            hot_dic_tran['user'] = user.username
                            hot_dic_tran['land_receive'] = trans_receives.count()
                if hot_dic_tran:
                    hot_data.append(hot_dic_tran)
        for attract in attracts:
            hot_dic_attract = {}
            luyou = '/tudimessage/zhaoshang'
            attract_receives = ReceivePeo.objects.filter(information_id=attract.id, luyou=luyou)
            if attract_receives:
                for attract_receive in attract_receives:
                    record = ReleaseRecord.objects.filter(land_id=attract.id, luyou=luyou).first()
                    if record:
                        user = Users.objects.filter(id=record.user_id).first()
                        if user:
                            hot_dic_attract['id'] = attract_receive.information_id
                            hot_dic_attract['title'] = attract.title
                            hot_dic_attract['luyou'] = attract_receive.luyou
                            hot_dic_attract['leibie'] = '招商信息'
                            hot_dic_attract['user'] = user.username
                            hot_dic_attract['land_receive'] = attract_receives.count()
                if hot_dic_attract:
                    hot_data.append(hot_dic_attract)
        return sorted(hot_data, key=operator.itemgetter('land_receive'), reverse=True)

    def get_collection_top(self):
        hot_data = []
        lands = LandInfo.objects.filter(create_on__gte=self.get_days(), create_on__lte=datetime.datetime.now(), audit_state=2)
        trans = TransInfo.objects.filter(create_on__gte=self.get_days(), create_on__lte=datetime.datetime.now(), audit_state=2)
        attracts = AttractInfo.objects.filter(create_on__gte=self.get_days(), create_on__lte=datetime.datetime.now(), audit_state=2)
        for land in lands:
            hot_dic_land = {}
            luyou = ['/tudimessage/nitui', '/tudimessage/paimai', '/tudimessage/guapai', '/tudimessage/xiancheng', ]
            land_collections = Collection.objects.filter(information_id=land.id, luyou__in=luyou)
            if land_collections:
                for land_collection in land_collections:
                    record = ReleaseRecord.objects.filter(land_id=land.id, luyou__in=luyou).first()
                    if record:
                        user = Users.objects.filter(id=record.user_id).first()
                        if user:
                            if land_collection.luyou == '/tudimessage/nitui':
                                l_luyou = '拟推预告'
                            elif land_collection.luyou == '/tudimessage/paimai':
                                l_luyou = '拍卖公告'
                            elif land_collection.luyou == '/tudimessage/guapai':
                                l_luyou = '挂牌公告'
                            elif land_collection.luyou == '/tudimessage/xiancheng':
                                l_luyou = '县城土地'
                            else:
                                l_luyou = 'a'
                            hot_dic_land['id'] = land_collection.information_id
                            hot_dic_land['title'] = land.title
                            hot_dic_land['luyou'] = land_collection.luyou
                            hot_dic_land['leibie'] = l_luyou
                            hot_dic_land['user'] = user.username
                            hot_dic_land['land_collection'] = land_collections.count()
                if hot_dic_land:
                    hot_data.append(hot_dic_land)
        for tran in trans:
            hot_dic_tran = {}
            luyou = '/tudimessage/zhuanrang'
            trans_collections = Collection.objects.filter(information_id=tran.id, luyou=luyou)
            if trans_collections:
                for trans_collection in trans_collections:
                    record = ReleaseRecord.objects.filter(land_id=tran.id, luyou=luyou).first()
                    if record:
                        user = Users.objects.filter(id=record.user_id).first()
                        if user:
                            hot_dic_tran['id'] = trans_collection.information_id
                            hot_dic_tran['title'] = tran.title
                            hot_dic_tran['luyou'] = trans_collection.luyou
                            hot_dic_tran['leibie'] = '转让信息'

                            hot_dic_tran['user'] = user.username
                            hot_dic_tran['land_collection'] = trans_collections.count()
                if hot_dic_tran:
                    hot_data.append(hot_dic_tran)
        for attract in attracts:
            hot_dic_attract = {}
            luyou = '/tudimessage/zhaoshang'
            attract_collections = Collection.objects.filter(information_id=attract.id, luyou=luyou)
            if attract_collections:
                for attract_collection in attract_collections:
                    record = ReleaseRecord.objects.filter(land_id=attract.id, luyou=luyou).first()
                    if record:
                        user = Users.objects.filter(id=record.user_id).first()
                        if user:
                            hot_dic_attract['id'] = attract_collection.information_id
                            hot_dic_attract['title'] = attract.title
                            hot_dic_attract['luyou'] = attract_collection.luyou
                            hot_dic_attract['leibie'] = '招商信息'

                            hot_dic_attract['user'] = user.username
                            hot_dic_attract['land_collection'] = attract_collections.count()
                if hot_dic_attract:
                    hot_data.append(hot_dic_attract)
        return sorted(hot_data, key=operator.itemgetter('land_collection'), reverse=True)

    def get_zan_top(self):
        hot_data = []
        trans = TransInfo.objects.filter(create_on__gte=self.get_days(), create_on__lte=datetime.datetime.now(), audit_state=2)
        for tran in trans:
            hot_dic_tran = {}
            trans_zans = Zan.objects.filter(land_id=tran.id, zc=1)
            if trans_zans:
                for trans_zan in trans_zans:
                    record = ReleaseRecord.objects.filter(land_id=tran.id, luyou='/tudimessage/zhuanrang').first()
                    if record:
                        user = Users.objects.filter(id=record.user_id).first()
                        if user:
                            hot_dic_tran['id'] = trans_zan.land_id
                            hot_dic_tran['title'] = tran.title
                            hot_dic_tran['luyou'] = trans_zan.luyou
                            hot_dic_tran['leibie'] = '转让信息'

                            hot_dic_tran['user'] = user.username
                            hot_dic_tran['land_zan'] = trans_zans.count()
                if hot_dic_tran:
                    hot_data.append(hot_dic_tran)
        return sorted(hot_data, key=operator.itemgetter('land_zan'), reverse=True)

    def get_cai_top(self):
        hot_data = []
        trans = TransInfo.objects.filter(create_on__gte=self.get_days(), create_on__lte=datetime.datetime.now(), audit_state=2)
        for tran in trans:
            hot_dic_tran = {}
            trans_cais = Zan.objects.filter(land_id=tran.id, zc=2)
            if trans_cais:
                for trans_cai in trans_cais:
                    record = ReleaseRecord.objects.filter(land_id=tran.id, luyou='/tudimessage/zhuanrang').first()
                    if record:
                        user = Users.objects.filter(id=record.user_id).first()
                        if user:
                            hot_dic_tran['id'] = trans_cai.land_id
                            hot_dic_tran['title'] = tran.title
                            hot_dic_tran['luyou'] = trans_cai.luyou
                            hot_dic_tran['leibie'] = '转让信息'

                            hot_dic_tran['user'] = user.username
                            hot_dic_tran['land_cai'] = trans_cais.count()
                if hot_dic_tran:
                    hot_data.append(hot_dic_tran)
        return sorted(hot_data, key=operator.itemgetter('land_cai'), reverse=True)

    def get(self, request):
        code = int(request.GET.get('code', 1))
        if code == 1:
            return Response({'hot_receive_data': self.get_receive_top(), 'status': '1'})
        elif code == 2:
            return Response({'hot_collection_top': self.get_collection_top(), 'status': '1'})
        elif code == 3:
            return Response({'hot_zan_top': self.get_zan_top(), 'status': '1'})
        elif code == 4:
            return Response({'hot_cai_top': self.get_cai_top(), 'status': '1'})
        else:
            return Response({'status': '0'})