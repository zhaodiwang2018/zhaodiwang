from rest_framework.views import APIView, Response
from apps.land.forms import *
from apps.land.serializers import *
from apps.utils.parsing import Parsing
from apps.utils.mixin_utils import LoginRequiredMixin
import datetime
import math
import os


# TODO:公告信息
class LandUpView(LoginRequiredMixin, APIView):
    """
    get:获取详情
    post：新建
    put：修改
    """

    def get(self, request):
        land_id = request.GET.get('land_id', 142)
        land = LandInfo.objects.filter(id=int(land_id))
        seria = ClientLandSerializers(land, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})

    def post(self, request):
        user_id = request.data.get('user_id')
        # 存放多张图片信息
        img_data = []
        img_lists = request.data.get('img_list')
        if img_lists:
            for img_list in img_lists:
                img_dic = {'status': 'success', 'uid': img_list['imgUid'],
                           'url': (Parsing(img_list['img64'], img_list['imgHZM']))}
                img_data.append(img_dic)
        user = Users.objects.filter(id=user_id).first()
        luyou = request.data.get('luyou')
        img = request.data.get('img')
        suffix_img = request.data.get('suffix_img')
        if suffix_img:
            img = Parsing(img, suffix_img)
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        form = NoticeClientForm(request.data)
        if suffix:
            file_url = Parsing(file_base, suffix)

        else:
            file_url = None
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if luyou == '/tudimessage/nitui':
                    land_type = 2
                elif luyou == '/tudimessage/guapai':
                    land_type = 1
                elif luyou == '/tudimessage/paimai':
                    land_type = 3
                elif luyou == '/tudimessage/xiancheng':
                    land_type = 4
                else:
                    land_type = 5
                land = LandInfo.objects.create(city=data['city'],
                                               land_type=land_type,
                                               area=data['area'],
                                               file_url=file_url,
                                               location=data['location'],
                                               serial_number=data['serial_number'],
                                               advance_date=data['advance_date'],
                                               listed_date=data['listed_date'],
                                               transfer_date=data['transfer_date'],
                                               land_nature=data['land_nature'],
                                               land_area=data['land_area'],
                                               plot_ratio=data['plot_ratio'],
                                               greening=data['greening'],
                                               building_density=data['building_density'],
                                               transfer_mode=data['transfer_mode'],
                                               margin=data['margin'],
                                               start_price=data['start_price'],
                                               transfer_high_price=data['transfer_high_price'],
                                               plan_condition=data['plan_condition'],
                                               remark=data['remark'],
                                               c_f=data['c_f'],
                                               title=data['title'],
                                               house_account=data['house_account'],
                                               content=data['content'],
                                               reward_price=data['reward_price'],
                                               img=img,
                                               desc=data['desc'],
                                               information_source=user.company,
                                               img_list=img_data,
                                               yuji_guapai=data['yuji_guapai'],
                                               now_progress=data['now_progress'],
                                               add_amplitude=data['add_amplitude'],
                                               special_requirements=data['special_requirements'],
                                               coordinates=data['coordinates'],
                                               pcc=data['pcc'],
                                               )

                ReleaseRecord.objects.create(user_id=user_id, land_id=land.id, luyou=luyou)
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功', 'id': land.id})
        return Response({'status': '0', 'msg': '数据不完整', 'data': form.errors})

    def put(self, request):
        land_id = request.data.get('land_id')
        img_data = []
        img_verifys = request.data.get('img_verify')
        if img_verifys:
            for img_verify in img_verifys:
                img_verify_dic = {'status': img_verify['status'], 'uid': img_verify['uid'],
                                  'url': img_verify['url'].split('/')[-1]}
                img_data.append(img_verify_dic)

        img_lists = request.data.get('img_list')
        if img_lists:
            for img_list in img_lists:
                img_dic = {'status': 'success', 'uid': img_list['imgUid'],
                           'url': (Parsing(img_list['img64'], img_list['imgHZM']))}
                img_data.append(img_dic)
        luyou = request.data.get('luyou')
        land = LandInfo.objects.filter(id=land_id).first()
        if land.img_list:
            for i in eval(land.img_list):
                if i not in img_data:
                    os.remove('/var/www/html/static/images/landimages/' + i['url'])
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        img_base = request.data.get('img_base')
        img_suffix = request.data.get('img_suffix')
        form = NoticeClientForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                land.city = data['city']
                land.area = data['area']
                if suffix:
                    if land.file_url:
                        os.remove('/var/www/html/static/images/landimages/' + land.file_url)
                    land.file_url = Parsing(file_base, suffix)
                land.location = data['location']
                land.serial_number = data['serial_number']
                land.advance_date = data['advance_date']
                land.listed_date = data['listed_date']
                land.transfer_date = data['transfer_date']
                land.land_nature = data['land_nature']
                land.land_area = data['land_area']
                land.plot_ratio = data['plot_ratio']
                land.greening = data['greening']
                land.building_density = data['building_density']
                land.transfer_mode = data['transfer_mode']
                land.margin = data['margin']
                land.reward_price = data['reward_price']
                land.start_price = data['start_price']
                land.transfer_high_price = data['transfer_high_price']
                land.plan_condition = data['plan_condition']
                land.remark = data['remark']
                land.house_account = data['house_account']
                land.c_f = data['c_f']
                land.title = data['title']
                land.content = data['content']
                land.img_list = img_data
                print(111)
                land.yuji_guapai = data['yuji_guapai']
                land.now_progress = data['now_progress']
                land.add_amplitude = data['add_amplitude']
                land.special_requirements = data['special_requirements']
                land.coordinates = data['coordinates']
                land.pcc = data['pcc']

                if img_suffix:
                    if land.img:
                        os.remove('/var/www/html/static/images/landimages/' + land.img)
                    land.img = Parsing(img_base, img_suffix)
                land.desc = data['desc']
                if luyou == '/tudimessage/nitui':
                    land.land_type = 2
                elif luyou == '/tudimessage/guapai':
                    land.land_type = 1
                elif luyou == '/tudimessage/paimai':
                    land.land_type = 3
                elif luyou == '/tudimessage/xiancheng':
                    land.land_type = 4
                else:
                    land.land_type = 5
                land.create_on = datetime.datetime.now()
                land.audit_state = 0
                land.save()

            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class NoticeEntryView(LoginRequiredMixin, APIView):
    """
    get: 公告列表
    post：下架
    """

    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        audit_state = request.GET.get('audit_state')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        if audit_state:
            condition['audit_state'] = int(audit_state)

        land_info = LandInfo.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = LandInfo.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = NoticeListSerializers(land_info, many=True)
        nitui_num = LandInfo.objects.filter(land_type='2').count()
        guapai_num = LandInfo.objects.filter(land_type='1').count()
        paimai_num = LandInfo.objects.filter(land_type='3').count()
        data_header = {'nitui_num': nitui_num, 'guapai_num': guapai_num, 'paimai_num': paimai_num}
        return Response(
            {'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page, 'data_header': data_header})

    def post(self, request):
        land_id = request.data.get('land_id')
        if not land_id:
            return Response({'status': '0', 'msg': '无id'})
        land = LandInfo.objects.filter(id=land_id).first()
        land.audit_state = 4
        land.save()
        return Response({'status': '1', 'msg': '下架成功'})


# TODO：转让信息
class TransUpView(LoginRequiredMixin, APIView):
    """
    get:获取详情
    post：新建
    put：修改
    """

    def get(self, request):
        land_id = request.GET.get('land_id', 8)
        trans = TransInfo.objects.filter(id=int(land_id))
        seria = ClientTransSerializers(trans, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})

    def post(self, request):
        user_id = request.data.get('user_id')
        img_data = []
        img_lists = request.data.get('img_list')
        if img_lists:
            for img_list in img_lists:
                img_dic = {'status': 'success', 'uid': img_list['imgUid'],
                           'url': (Parsing(img_list['img64'], img_list['imgHZM']))}
                img_data.append(img_dic)
        user = Users.objects.filter(id=user_id).first()
        img = request.data.get('img')
        suffix_img = request.data.get('suffix_img')
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        form = TransClientForm(request.data)
        if suffix:
            file_url = Parsing(file_base, suffix)
        else:
            file_url = None
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if img:
                    img = Parsing(img, suffix_img)
                trans = TransInfo.objects.create(city=data['city'],
                                                 area=data['area'],
                                                 file_url=file_url,
                                                 location=data['location'],
                                                 serial_number=data['serial_number'],
                                                 land_nature=data['land_nature'],
                                                 land_area=data['land_area'],
                                                 plot_ratio=data['plot_ratio'],
                                                 reward_price=data['reward_price'],
                                                 greening=data['greening'],
                                                 building_density=data['building_density'],
                                                 trading_type=data['trading_type'],
                                                 deposit=data['deposit'],
                                                 price=data['price'],
                                                 people=data['people'],
                                                 contact=data['contact'],
                                                 licensor=data['licensor'],
                                                 plan_conditions=data['plan_conditions'],
                                                 trading_conditions=data['trading_conditions'],
                                                 title=data['title'],
                                                 content=data['content'],
                                                 house_account=data['house_account'],
                                                 remark=data['remark'],
                                                 img=img,
                                                 desc=data['desc'],
                                                 information_source=user.company,
                                                 img_list=img_data,
                                                 information_validity=data['information_validity'],
                                                 coordinates=data['coordinates'],
                                                 pcc=data['pcc'],

                                                 )
                ReleaseRecord.objects.create(user_id=user_id, land_id=trans.id, luyou='/tudimessage/zhuanrang')
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功', 'id': trans.id})
        return Response({'status': '0', 'msg': '数据不完整', 'data': form.errors})

    def put(self, request):
        land_id = request.data.get('land_id')
        img_data = []
        img_verifys = request.data.get('img_verify')
        if img_verifys:
            for img_verify in img_verifys:
                img_verify_dic = {'status': img_verify['status'], 'uid': img_verify['uid'],
                                  'url': img_verify['url'].split('/')[-1]}
                img_data.append(img_verify_dic)
                # a_data.append(img_verify_dic)

        img_lists = request.data.get('img_list')
        if img_lists:
            for img_list in img_lists:
                img_dic = {'status': 'success', 'uid': img_list['imgUid'],
                           'url': (Parsing(img_list['img64'], img_list['imgHZM']))}
                img_data.append(img_dic)
        trans = TransInfo.objects.filter(id=land_id).first()
        if trans.img_list:
            for i in eval(trans.img_list):
                if i not in img_data:
                    os.remove('/var/www/html/static/images/landimages/' + i['url'])
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        img_base = request.data.get('img_base')
        img_suffix = request.data.get('img_suffix')
        form = TransClientForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                trans.city = data['city']
                trans.area = data['area']
                if suffix:
                    if trans.file_url:
                        os.remove('/var/www/html/static/images/landimages/' + trans.file_url)
                    trans.file_url = Parsing(file_base, suffix)
                trans.location = data['location']
                trans.serial_number = data['serial_number']
                trans.land_nature = data['land_nature']
                trans.land_area = data['land_area']
                trans.plot_ratio = data['plot_ratio']
                trans.greening = data['greening']
                trans.reward_price = data['reward_price']
                trans.building_density = data['building_density']
                trans.trading_type = data['trading_type']
                trans.deposit = data['deposit']
                trans.price = data['price']
                trans.people = data['people']
                trans.contact = data['contact']
                trans.licensor = data['licensor']
                trans.plan_conditions = data['plan_conditions']
                trans.trading_conditions = data['trading_conditions']
                trans.title = data['title']
                trans.house_account = data['house_account']
                trans.remark = data['remark']
                trans.content = data['content']
                trans.coordinates = data['coordinates']
                trans.pcc = data['pcc']

                if img_suffix:
                    if trans.img:
                        os.remove('/var/www/html/static/images/landimages/' + trans.img)
                    trans.img = Parsing(img_base, img_suffix)
                trans.desc = data['desc']
                trans.img_list = img_data
                trans.information_validity = data['information_validity']
                trans.create_on = datetime.datetime.now()
                trans.audit_state = 0
                trans.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


# TODO：转让列表
class TransEntryView(LoginRequiredMixin, APIView):
    """
    get: 装让列表
    post：下架
    """

    def get(self, request):
        page = int(request.GET.get('page', 1))
        audit_state = request.GET.get('audit_state')
        create_on = request.GET.get('create_on')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        if audit_state:
            condition['audit_state'] = int(audit_state)
        trans_info = TransInfo.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = TransInfo.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = TransInfoListSerializers(trans_info, many=True)
        zhuanrang_num = TransInfo.objects.all().count()
        data_header = {'zhuanrang_num': zhuanrang_num}

        return Response(
            {'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page, 'data_header': data_header})

    def post(self, request):
        land_id = request.data.get('land_id')
        if not land_id:
            return Response({'status': '0', 'msg': '无id'})
        land = TransInfo.objects.filter(id=land_id).first()
        land.audit_state = 4
        land.save()
        return Response({'status': '1', 'msg': '下架成功'})


# TODO:招商信息
class AttractUpView(LoginRequiredMixin, APIView):
    """
    get:获取详情
    post：新建
    put：修改
    """

    def get(self, request):
        land_id = request.GET.get('land_id', 7)
        attract = AttractInfo.objects.filter(id=int(land_id))
        seria = ClientAttractSerializers(attract, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})

    def post(self, request):
        user_id = request.data.get('user_id')
        img_data = []
        img_lists = request.data.get('img_list')
        if img_lists:
            for img_list in img_lists:
                img_dic = {'status': 'success', 'uid': img_list['imgUid'],
                           'url': (Parsing(img_list['img64'], img_list['imgHZM']))}
                img_data.append(img_dic)
        user = Users.objects.filter(id=user_id).first()
        img = request.data.get('img')
        suffix_img = request.data.get('suffix_img')
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        form = AttractClientForm(request.data)
        if suffix:
            file_url = Parsing(file_base, suffix)
        else:
            file_url = None
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                if img:
                    img = Parsing(img, suffix_img)
                attract = AttractInfo.objects.create(city=data['city'],
                                                     area=data['area'],
                                                     file_url=file_url,
                                                     location=data['location'],
                                                     serial_number=data['serial_number'],
                                                     notice_date=data['notice_date'],
                                                     land_nature=data['land_nature'],
                                                     land_area=data['land_area'],
                                                     total_inv=data['total_inv'],
                                                     people=data['people'],
                                                     plot_ratio=data['plot_ratio'],
                                                     contact=data['contact'],
                                                     cooperate_condition=data['cooperate_condition'],
                                                     title=data['title'],
                                                     content=data['content'],
                                                     remark=data['remark'],
                                                     reward_price=data['reward_price'],
                                                     house_account=data['house_account'],
                                                     img=img,
                                                     desc=data['desc'],
                                                     information_source=user.company,
                                                     img_list=img_data,
                                                     industry_requirements=data['industry_requirements'],
                                                     coordinates=data['coordinates'],
                                                     pcc=data['pcc'],

                                                     )
                ReleaseRecord.objects.create(user_id=user_id, land_id=attract.id, luyou='/tudimessage/zhaoshang')
                # users = Users.objects.filter(city__contains=attract.city)
                # for user in users:
                #     YaoQing.objects.create(user_id=user.id, land_id=attract.id, luyou='/tudimessage/zhaoshang')
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功', 'id': attract.id})
        return Response({'status': '0', 'msg': '数据不完整', 'data': form.errors})

    def put(self, request):
        land_id = request.data.get('land_id')
        img_data = []
        img_verifys = request.data.get('img_verify')
        if img_verifys:
            for img_verify in img_verifys:
                img_verify_dic = {'status': img_verify['status'], 'uid': img_verify['uid'],
                                  'url': img_verify['url'].split('/')[-1]}
                img_data.append(img_verify_dic)

        img_lists = request.data.get('img_list')
        if img_lists:
            for img_list in img_lists:
                img_dic = {'status': 'success', 'uid': img_list['imgUid'],
                           'url': (Parsing(img_list['img64'], img_list['imgHZM']))}
                img_data.append(img_dic)
        attract = AttractInfo.objects.filter(id=land_id).first()
        if attract.img_list:
            for i in eval(attract.img_list):
                if i not in img_data:
                    os.remove('/var/www/html/static/images/landimages/' + i['url'])
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        img_base = request.data.get('img_base')
        img_suffix = request.data.get('img_suffix')
        form = AttractClientForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                attract.city = data['city']
                attract.area = data['area']
                if suffix:
                    if attract.file_url:
                        os.remove('/var/www/html/static/images/landimages/' + attract.file_url)
                    attract.file_url = Parsing(file_base, suffix)
                attract.location = data['location']
                attract.serial_number = data['serial_number']
                attract.land_nature = data['land_nature']
                attract.land_area = data['land_area']
                attract.cooperate_condition = data['cooperate_condition']
                attract.people = data['people']
                attract.contact = data['contact']
                attract.notice_date = data['notice_date']
                attract.total_inv = data['total_inv']
                attract.house_account = data['house_account']
                attract.title = data['title']
                attract.content = data['content']
                attract.remark = data['remark']
                attract.reward_price = data['reward_price']
                attract.plot_ratio = data['plot_ratio']
                attract.coordinates = data['coordinates']
                attract.pcc = data['pcc']
                if img_suffix:
                    if attract.img:
                        os.remove('/var/www/html/static/images/landimages/' + attract.img)
                    attract.img = Parsing(img_base, img_suffix)
                attract.desc = data['desc']
                attract.img_list = img_data
                attract.industry_requirements = data['industry_requirements']
                attract.create_on = datetime.datetime.now()
                attract.audit_state = 0
                attract.save()

            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


# TODO：招商列表
class AttractEntryView(LoginRequiredMixin, APIView):
    """
    get:招商列表
    post:下架
    """

    def get(self, request):

        page = int(request.GET.get('page', 1))
        audit_state = request.GET.get('audit_state')
        create_on = request.GET.get('create_on')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        if audit_state:
            condition['audit_state'] = int(audit_state)
        attract_info = AttractInfo.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = AttractInfo.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = AttractListSerializers(attract_info, many=True)
        zhaoshang_num = AttractInfo.objects.all().count()
        data_header = {'zhaoshang_num': zhaoshang_num}
        return Response(
            {'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page, 'data_header': data_header})

    def post(self, request):
        land_id = request.data.get('land_id')
        if not land_id:
            return Response({'status': '0', 'msg': '无id'})
        land = AttractInfo.objects.filter(id=land_id).first()
        land.audit_state = 4
        land.save()
        return Response({'status': '1', 'msg': '下架成功'})
