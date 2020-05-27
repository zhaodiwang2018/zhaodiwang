from rest_framework.views import APIView, Response
from apps.land.serializers import *
from apps.user.models import *
from apps.land.forms import *
from apps.utils.parsing import Parsing
from apps.utils.mixin_utils import *
import os
import math
import operator
import datetime


# user = Users.objects.filter(mobile=get_user_id(request)).first()
import time, functools
def metric(fn):
    # print(1)
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        time0 = time.time()
        ret = fn(*args, **kw)
        time1 = time.time()
        print('%s executed in %s ms' % (fn.__name__, time1-time0))
        return ret
    # print(5)
    return wrapper

# TODO:收藏功能
# @metric
class CollectionView(LoginRequiredMixin, APIView):
    """
    post: 收藏
    delete：取消收藏
    """

    @metric
    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        user_id = user.id
        luyou = request.data.get('luyou')
        information_id = request.data.get('information_id')
        Collection.objects.create(user_id=user_id, luyou=luyou, information_id=information_id)
        today = datetime.date.today()
        today_data = AdminUserChart.objects.filter(create_on=today).first()
        if today_data:
            today_data.today_shoucang += 1
            today_data.save()
        else:
            user_num = Users.objects.count()
            AdminUserChart.objects.create(today_shoucang=1, user_all=user_num)
        if user.usertype == '1':
            paiming_user = PaiMing.objects.first(user_id=user.id).first()
            paiming_user.act_num += 0.1
            paiming_user.save()
        return Response({'msg': '收藏成功', 'status': '1'})

    def delete(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        user_id = user.id
        luyou = request.data.get('luyou')
        information_id = request.data.get('information_id')
        res = Collection.objects.filter(luyou=luyou, user_id=user_id, information_id=information_id).first()
        if res:
            res.delete()
            today = datetime.date.today()
            today_data = AdminUserChart.objects.filter(create_on=today).first()
            if today_data:
                today_data.today_shoucang -= 1
                today_data.save()
            if user.usertype == '1':
                paiming_user = PaiMing.objects.first(user_id=user.id).first()
                paiming_user.act_num -= 0.1
                paiming_user.save()

            return Response({'msg': '取消收藏成功', 'status': '1'})
        return Response({'msg': '取消收藏失败', 'status': '0'})


# TODO：发布记录
class ReleaseRecordDetailView(LoginRequiredMixin, APIView):

    def get(self, request):
        luyou = request.GET.get('luyou')
        land_id = request.GET.get('land_id')
        number = request.GET.get('number')
        rele = ReleaseRecord.objects.filter(land_id=land_id, luyou=luyou).first()
        user = Users.objects.filter(id=rele.user_id).first()
        if number == '1':
            yaoqing = YaoQing.objects.filter(luyou=luyou, land_id=land_id).order_by('-id')
            seria = FaBuYaoqingSerializers(yaoqing, many=True)
            return Response({'msg': '成功', 'status': '1', 'data': seria.data, })
        elif number == '2':
            chakan = ReceivePeo.objects.filter(luyou=luyou, information_id=land_id).order_by('-id')
            seria = FaBuChakanSerializers(chakan, many=True)
            return Response({'msg': '成功', 'status': '1', 'data': seria.data, })
        elif number == '3':
            shoucang = Collection.objects.filter(luyou=luyou, information_id=land_id).order_by('-id')
            seria = FaBuShoucangSerializers(shoucang, many=True)
            return Response({'msg': '成功', 'status': '1', 'data': seria.data, })
        elif number == '4':
            lianxi = Contact.objects.filter(contacted_id=user.id, luyou=luyou, land_id=land_id)
            seria = FaBuLianxiSerializers(lianxi, many=True)
            return Response({'msg': '成功', 'status': '1', 'data': seria.data, })
        elif number == '5':
            lianxi = Contact.objects.filter(contacted_id=user.id, luyou=luyou, land_id=land_id)
            seria = FaBuLianxiSerializers(lianxi, many=True)
            return Response({'msg': '成功', 'status': '1', 'data': seria.data, })
        elif number == '6':
            zan = Zan.objects.filter(luyou=luyou, land_id=land_id, zc=1).order_by('-id')
            seria = FaBuZanSerializers(zan, many=True)
            return Response({'msg': '成功', 'status': '1', 'data': seria.data, })
        elif number == '7':
            cai = Zan.objects.filter(luyou=luyou, land_id=land_id, zc=2).order_by('-id')
            seria = FaBuZanSerializers(cai, many=True)
            return Response({'msg': '成功', 'status': '1', 'data': seria.data, })
        return Response({'msg': '获取成功', 'status': '1', })


# TODO:后端土地信息列表
class LandDataListView(LoginRequiredMixin, APIView):

    def get(self, request):
        page = int(request.GET.get('page', 1))

        create_on = request.GET.get('create_on')
        audit_state = request.GET.get('audit_state', 2)
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        if audit_state:
            condition['audit_state'] = int(audit_state)
        land_info = LandInfo.objects.filter(**condition)
        seria_land = NoticeListSerializers(land_info, many=True)
        trans_info = TransInfo.objects.filter(**condition)
        seria_trans = TransInfoListSerializers(trans_info, many=True)
        attract_info = AttractInfo.objects.filter(**condition)
        seria_attract = AttractListSerializers(attract_info, many=True)
        q_data = seria_land.data + seria_trans.data + seria_attract.data
        data = sorted(q_data, key=operator.itemgetter('create_on'), reverse=True)
        count = len(data)
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        nitui_num = LandInfo.objects.filter(land_type='2').count()
        guapai_num = LandInfo.objects.filter(land_type='1').count()
        paimai_num = LandInfo.objects.filter(land_type='3').count()
        zhuanrang_num = TransInfo.objects.all().count()
        zhaoshang_num = AttractInfo.objects.all().count()
        data_header = {'nitui_num': nitui_num, 'guapai_num': guapai_num, 'paimai_num': paimai_num,
                       'zhuanrang_num': zhuanrang_num, 'zhaoshang_num': zhaoshang_num}
        return Response(
            {'data': data[(page - 1) * 8:(page - 1) * 8 + 8], 'data_header': data_header, 'msg': '成功', 'status': '1',
             'total_page': total_page})


# TODO:新建找地活动
class ActivityInfoView(LoginRequiredMixin, APIView):
    def get(self, request):
        land_id = request.GET.get('land_id', 7)
        activity = Activity.objects.filter(id=int(land_id))
        seria = ActivityDetailSerializers(activity, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})

    def post(self, request):
        global activity_type
        luyou = request.data.get('luyou')
        user_id = request.data.get('user_id')
        img = request.data.get('img')
        suffix = request.data.get('suffix')
        form = ActivityInformationForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if luyou == '/activity/shalong':
                    activity_type = 1
                elif luyou == '/activity/yuebao':
                    activity_type = 2
                elif luyou == '/activity/tuijie':
                    activity_type = 3
                elif luyou == '/activity/kuanian':
                    activity_type = 4
                else:
                    pass
                img = Parsing(img, suffix)
                activity = Activity.objects.create(title=data['title'],
                                                   content=data['content'],
                                                   img=img,
                                                   desc=data['desc'],
                                                   reward_price=data['reward_price'],
                                                   information_source=data['information_source'],
                                                   activity_datetime=data['activity_datetime'],
                                                   activity_place=data['activity_place'],
                                                   activity_type=activity_type,
                                                   content_feed=data['content_feed'],
                                                   traffic_tips=data['traffic_tips'],
                                                   quota=data['quota'],

                                                   )
                ReleaseRecord.objects.create(user_id=user_id, land_id=activity.id, luyou=luyou)

            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})

    def put(self, request):
        land_id = request.data.get('land_id')
        luyou = request.data.get('luyou')
        activity = Activity.objects.filter(id=land_id).first()
        img = request.data.get('img')
        suffix = request.data.get('suffix')
        form = ActivityInformationForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if luyou == '/activity/shalong':
                    activity_types = 1
                elif luyou == '/activity/yuebao':
                    activity_types = 2
                elif luyou == '/activity/tuijie':
                    activity_types = 3
                elif luyou == '/activity/kuanian':
                    activity_types = 4
                else:
                    activity_types = 0
                activity.title = data['title']
                activity.content = data['content']
                if suffix:
                    os.remove('/var/www/html/static/images/landimages/' + activity.img)
                    activity.img = Parsing(img, suffix)
                activity.desc = data['desc']
                activity.reward_price = data['reward_price']
                activity.information_source = data['information_source']
                activity.activity_datetime = data['activity_datetime']
                activity.activity_place = data['activity_place']
                activity.activity_type = activity_types
                activity.content_feed = data['content_feed']
                activity.quota = data['quota']
                activity.traffic_tips = data['traffic_tips']
                activity.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class ActivityDeleteView(LoginRequiredMixin, APIView):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        audit_state = request.GET.get('audit_state')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        if audit_state:
            condition['audit_state'] = int(audit_state)

        land_info = Activity.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = Activity.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = ActivitySerializers(land_info, many=True)
        shalong_num = Activity.objects.filter(activity_type='1').count()
        yuebao_num = Activity.objects.filter(activity_type='2').count()
        tuijiehui_num = Activity.objects.filter(activity_type='3').count()
        data_header = {'shalong_num': shalong_num, 'yuebao_num': yuebao_num, 'tuijiehui_num': tuijiehui_num}
        return Response(
            {'data': seria.data, 'data_header': data_header, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        land_id = request.data.get('land_id')
        if not land_id:
            return Response({'status': '0', 'msg': '无id'})
        land = Activity.objects.filter(id=land_id).first()
        land.audit_state = 4
        land.save()
        return Response({'status': '1', 'msg': '下架成功'})


class PropertyListView(LoginRequiredMixin, APIView):

    def get(self, request):
        land_id = request.GET.get('land_id', 7)
        poplist = PropertyList.objects.filter(id=int(land_id))
        seria = PropertyListDetailSerializers(poplist, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})

    def post(self, request):
        global property_type
        luyou = request.data.get('luyou')
        user_id = request.data.get('user_id')
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        img_base = request.data.get('img_base')
        img_suffix = request.data.get('img_suffix')
        form = PropertyInformationForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if luyou == "/tudilist/nadi":
                    property_type = 1
                elif luyou == "/tudilist/gongdi":
                    property_type = 2
                elif luyou == "/tudilist/shoulou":
                    property_type = 3
                elif luyou == "/tudilist/loupan":
                    property_type = 4
                else:
                    pass
                img = Parsing(img_base, img_suffix)
                file_url = Parsing(file_base, suffix)
                poplist = PropertyList.objects.create(title=data['title'],
                                                      content=data['content'],
                                                      img=img,
                                                      desc=data['desc'],
                                                      reward_price=data['reward_price'],
                                                      information_source=data['information_source'],
                                                      property_type=property_type,
                                                      file_url=file_url,
                                                      file_introduction=data['file_introduction']
                                                      )
                ReleaseRecord.objects.create(user_id=user_id, land_id=poplist.id, luyou=luyou)
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})

    def put(self, request):
        land_id = request.data.get('land_id')
        poplist = PropertyList.objects.filter(id=land_id).first()
        luyou = request.data.get('luyou')
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        img_base = request.data.get('img_base')
        img_suffix = request.data.get('img_suffix')
        form = PropertyInformationForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if luyou == "/tudilist/nadi":
                    property_types = 1
                elif luyou == "/tudilist/gongdi":
                    property_types = 2
                elif luyou == "/tudilist/shoulou":
                    property_types = 3
                elif luyou == "/tudilist/loupan":
                    property_types = 4
                else:
                    property_types = 0
                poplist.title = data['title']
                poplist.content = data['content']
                if img_suffix:
                    os.remove('/var/www/html/static/images/landimages/' + poplist.img)
                    poplist.img = Parsing(img_base, img_suffix)
                poplist.desc = data['desc']
                poplist.reward_price = data['reward_price']
                poplist.information_source = data['information_source']
                poplist.property_type = property_types
                if suffix:
                    os.remove('/var/www/html/static/images/landimages/' + poplist.file_url)
                    poplist.file_url = Parsing(file_base, suffix)

                poplist.file_introduction = data['file_introduction']
                poplist.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class PopListDeleteView(LoginRequiredMixin, APIView):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        audit_state = request.GET.get('audit_state')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        if audit_state:
            condition['audit_state'] = int(audit_state)

        land_info = PropertyList.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = PropertyList.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = PopListSerializers(land_info, many=True)
        nadi_num = PropertyList.objects.filter(property_type='1').count()
        gongdi_num = PropertyList.objects.filter(property_type='2').count()
        shoufang_num = PropertyList.objects.filter(property_type='3').count()
        data_header = {'nadi_num': nadi_num, 'gongdi_num': gongdi_num, 'shoufang_num': shoufang_num}
        return Response(
            {'data': seria.data, 'data_header': data_header, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        land_id = request.data.get('land_id')
        if not land_id:
            return Response({'status': '0', 'msg': '无id'})
        land = PropertyList.objects.filter(id=land_id).first()
        land.audit_state = 4
        land.save()
        return Response({'status': '1', 'msg': '下架成功'})


class InvestmentDataView(LoginRequiredMixin, APIView):

    def get(self, request):
        land_id = request.GET.get('land_id', 7)
        poplist = InvestmentData.objects.filter(id=int(land_id))
        seria = InvestmentDataDetailSerializers(poplist, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})

    def post(self, request):
        global property_type
        luyou = request.data.get('luyou')
        user_id = request.data.get('user_id')
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        img_base = request.data.get('img_base')
        img_suffix = request.data.get('img_suffix')
        form = InvestmentInformationForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if luyou == "/Investment/zhoubao":
                    property_type = 1
                elif luyou == "/Investment/yuebao":
                    property_type = 2
                elif luyou == "/Investment/jibao":
                    property_type = 3
                elif luyou == "/Investment/bannianbao":
                    property_type = 4
                elif luyou == "/Investment/nianbao":
                    property_type = 5
                else:
                    pass
                img = Parsing(img_base, img_suffix)
                file_url = Parsing(file_base, suffix)
                invdata = InvestmentData.objects.create(title=data['title'],
                                                        content=data['content'],
                                                        img=img,
                                                        desc=data['desc'],
                                                        reward_price=data['reward_price'],
                                                        information_source=data['information_source'],
                                                        property_type=property_type,
                                                        file_url=file_url,
                                                        file_introduction=data['file_introduction']
                                                        )
                ReleaseRecord.objects.create(user_id=user_id, land_id=invdata.id, luyou=luyou)
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})

    def put(self, request):
        land_id = request.data.get('land_id')
        user_id = request.data.get('user_id')
        inv = InvestmentData.objects.filter(id=land_id).first()
        luyou = request.data.get('luyou')
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        img_base = request.data.get('img_base')
        img_suffix = request.data.get('img_suffix')
        form = InvestmentInformationForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if luyou == "/Investment/zhoubao":
                    property_types = 1
                elif luyou == "/Investment/yuebao":
                    property_types = 2
                elif luyou == "/Investment/jibao":
                    property_types = 3
                elif luyou == "/Investment/bannianbao":
                    property_types = 4
                elif luyou == "/Investment/nianbao":
                    property_types = 5
                else:
                    property_types = 0
                inv.title = data['title']
                inv.content = data['content']
                if img_suffix:
                    os.remove('/var/www/html/static/images/landimages/' + inv.img)
                    inv.img = Parsing(img_base, img_suffix)
                inv.desc = data['desc']
                inv.reward_price = data['reward_price']
                inv.information_source = data['information_source']
                inv.property_type = property_types
                if suffix:
                    os.remove('/var/www/html/static/images/landimages/' + inv.file_url)
                    inv.file_url = Parsing(file_base, suffix)
                inv.file_introduction = data['file_introduction']
                inv.save()
                ReleaseRecord.objects.create(user_id=user_id, land_id=inv.id, luyou=luyou)
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class InvestmentDataDeleteView(LoginRequiredMixin, APIView):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        audit_state = request.GET.get('audit_state')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        if audit_state:
            condition['audit_state'] = int(audit_state)

        land_info = InvestmentData.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = InvestmentData.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = InvestmentDataListSerializers(land_info, many=True)
        zhoubao_num = InvestmentData.objects.filter(property_type='1').count()
        yuebao_num = InvestmentData.objects.filter(property_type='2').count()
        data_header = {'zhoubao_num': zhoubao_num, 'yuebao_num': yuebao_num}

        return Response({'data': seria.data, 'data_header':data_header,'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        land_id = request.data.get('land_id')
        if not land_id:
            return Response({'status': '0', 'msg': '无id'})
        land = InvestmentData.objects.filter(id=land_id).first()
        land.audit_state = 4
        land.save()
        return Response({'status': '1', 'msg': '下架成功'})


class YaoqingDetailView(APIView):

    def get(self, request):
        yaoqing_id = request.GET.get('yaoqing_id', 1)
        user_id = request.GET.get('user_id', 1)
        if not YaoQingRead.objects.filter(yaoqing_id=yaoqing_id, user_id=user_id).first():
            YaoQingRead.objects.create(yaoqing_id=yaoqing_id, user_id=user_id)
        return Response({'result': '1', 'message': '获取邀请成功'})


# 手机端个人中心四个数字（取第一个）
class Mse(APIView):
    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        user_id = user.id
        data = {}
        nitui_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/nitui', user_id=user_id, ).count()
        paimai_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/paimai', user_id=user_id, ).count()
        guapai_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/guapai', user_id=user_id, ).count()
        zhuanrang_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/zhuanrang', user_id=user_id, ).count()
        zhaoshang_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/zhaoshang', user_id=user_id, ).count()
        xiancheng_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/xiancheng', user_id=user_id, ).count()
        shalong_yaoqing_num = YaoQing.objects.filter(user_id=user_id, luyou='/activity/shalong').count()
        yue_yaoqing_num = YaoQing.objects.filter(luyou='/activity/yuebao', user_id=user_id, ).count()
        tuijie_yaoqing_num = YaoQing.objects.filter(luyou='/activity/tuijie', user_id=user_id, ).count()
        nadi_yaoqing_num = YaoQing.objects.filter(luyou="/tudilist/nadi", user_id=user_id, ).count()
        gongdi_yaoqing_num = YaoQing.objects.filter(luyou='/tudilist/gongdi', user_id=user_id, ).count()
        shoulou_yaoqing_num = YaoQing.objects.filter(luyou='/tudilist/shoulou', user_id=user_id, ).count()
        loupan_yaoqing_num = YaoQing.objects.filter(luyou='/tudilist/loupan', user_id=user_id, ).count()
        zhoubao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/zhoubao", user_id=user_id, ).count()
        yuebao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/yuebao", user_id=user_id, ).count()
        jibao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/jibao", user_id=user_id, ).count()
        bannianbao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/bannianbao", user_id=user_id, ).count()
        nianbao_yaoqing_num = YaoQing.objects.filter(luyou="/Investment/nianbao", user_id=user_id, ).count()
        data[
            '311'] = nitui_receive_num + paimai_receive_num + guapai_receive_num + zhuanrang_receive_num + zhaoshang_receive_num + xiancheng_receive_num
        data['411'] = shalong_yaoqing_num + yue_yaoqing_num + tuijie_yaoqing_num
        data['511'] = nadi_yaoqing_num + gongdi_yaoqing_num + shoulou_yaoqing_num + loupan_yaoqing_num
        data[
            '611'] = zhoubao_yaoqing_num + yuebao_yaoqing_num + jibao_yaoqing_num + bannianbao_yaoqing_num + nianbao_yaoqing_num
        return Response({'data': data, 'msg': '成功', 'status': '1'})
