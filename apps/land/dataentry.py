from rest_framework.views import APIView, Response
from apps.land.serializers import *
from apps.land.forms import *
from apps.utils.parsing import Parsing
from apps.utils.mixin_utils import LoginRequiredMixin

import math
import datetime


# TODO：成交信息
class DealView(LoginRequiredMixin, APIView):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        condition = {'is_deal': 1}
        if create_on:
            condition['create_on'] = create_on
        deal_info = LandInfo.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = LandInfo.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = DealListSerializers(deal_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        form = DealForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            land = LandInfo.objects.filter(serial_number=data['serial_number']).first()
            if not land:
                return Response({'status': '0', 'msg': '无此编号'})
            try:
                land.deal_time = data['deal_time']
                land.deal_money = data['deal_money']
                land.deal_remark = data['deal_remark']
                land.is_deal = 1
                land.transferee_peo = data['transferee_peo']
                land.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class DealIdView(LoginRequiredMixin, APIView):
    def get(self, request):
        d_id = request.GET.get('id', 38)
        if not d_id:
            return Response({'status': '0', 'msg': '无id'})
        deal = LandInfo.objects.filter(id=d_id)
        seria = DealListSerializers(deal, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})


# TODO：收并购
class InvChargeMergeView(LoginRequiredMixin, APIView):

    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        invchargemerge_info = InvChargeMerge.objects.filter(**condition).order_by('-id')[
                              (page - 1) * 8:(page - 1) * 8 + 8]
        count = InvChargeMerge.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = InvChargeMergeListSerializers(invchargemerge_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        form = InvChargeMergeForm(request.data)
        if suffix:
            file_url = Parsing(file_base, suffix)
        else:
            file_url = None
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                InvChargeMerge.objects.create(
                    city=data['city'],
                    area=data['area'],
                    file_url=file_url,
                    location=data['location'],
                    serial_number=data['serial_number'],
                    land_nature=data['land_nature'],
                    land_area=data['land_area'],
                    plot_ratio=data['plot_ratio'],
                    building_density=data['building_density'],
                    trading_type=data['trading_type'],
                    deposit=data['deposit'],
                    price=data['price'],
                    deal_money=data['deal_money'],
                    transferee_peo=data['transferee_peo'],
                    licensor=data['licensor'],
                    plan_conditions=data['plan_conditions'],
                    trading_conditions=data['trading_conditions']
                )
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})

    def put(self, request):
        i_id = request.data.get('id')
        charge = InvChargeMerge.objects.filter(id=i_id).first()
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        file_url = request.data.get('file_url')
        form = InvChargeMergeForm(request.data)
        if suffix:
            file_url = Parsing(file_base, suffix)
        else:
            file_url = file_url
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                charge.city = data['city']
                charge.area = data['area']
                charge.file_url = file_url
                charge.location = data['location']
                charge.serial_number = data['serial_number']
                charge.land_nature = data['land_nature']
                charge.land_area = data['land_area']
                charge.plot_ratio = data['plot_ratio']
                charge.building_density = data['building_density']
                charge.trading_type = data['trading_type']
                charge.deposit = data['deposit']
                charge.price = data['price']
                charge.deal_money = data['deal_money']
                charge.transferee_peo = data['transferee_peo']
                charge.licensor = data['licensor']
                charge.plan_conditions = data['plan_conditions']
                charge.trading_conditions = data['trading_conditions']
                charge.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'}),


class InvChargeMergeIdView(LoginRequiredMixin, APIView):
    def get(self, request):
        i_id = request.GET.get('id', 38)
        if not i_id:
            return Response({'status': '0', 'msg': '无id'})
        charge = InvChargeMerge.objects.filter(id=i_id)
        seria = InvChargeMergeListSerializers(charge, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})


# TODO：楼市供应
class BuildingSupplyFView(LoginRequiredMixin, APIView):

    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        supply_info = BuildingSupplyF.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = BuildingSupplyF.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = BuildingSupplyListSerializers(supply_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        form = BuildingSupplyForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                BuildingSupplyF.objects.create(
                    city=data['city'],
                    acreage=data['acreage'],
                    tao_num=data['tao_num'],
                    project_num=data['project_num']
                )
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})
    def put(self, request):
        f_id = request.data.get('id')
        supply_f = BuildingSupplyF.objects.filter(id=f_id).first()
        form = BuildingSupplyForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                supply_f.city = data['city']
                supply_f.acreage = data['acreage']
                supply_f.tao_num = data['tao_num']
                supply_f.project_num = data['project_num']
                supply_f.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class BuildingSupplyFIdView(LoginRequiredMixin, APIView):
    def get(self, request):
        s_id = request.GET.get('id', 38)
        if not s_id:
            return Response({'status': '0', 'msg': '无id'})
        supply = BuildingSupplyF.objects.filter(id=s_id)
        seria = BuildingSupplyListSerializers(supply, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})


# TODO：楼市成交
class BuildingSupplyTView(LoginRequiredMixin, APIView):

    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        supplyt_info = BuildingSupplyT.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = BuildingSupplyT.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = BuildingSupplyTListSerializers(supplyt_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        form = BuildingSupplyTForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                BuildingSupplyT.objects.create(
                    city=data['city'],
                    acreage=data['acreage'],
                    tao_num=data['tao_num'],
                    project_num=data['project_num']
                )
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})
    def put(self, request):
        t_id = request.data.get('id')
        supply_t = BuildingSupplyT.objects.filter(id=t_id).first()
        form = BuildingSupplyTForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                supply_t.city = data['city']
                supply_t.acreage = data['acreage']
                supply_t.tao_num = data['tao_num']
                supply_t.project_num = data['project_num']
                supply_t.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class BuildingSupplyTIdView(LoginRequiredMixin, APIView):
    def get(self, request):
        b_id = request.GET.get('id', 38)
        if not b_id:
            return Response({'status': '0', 'msg': '无id'})
        supply = BuildingSupplyT.objects.filter(id=b_id)
        seria = BuildingSupplyTListSerializers(supply, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})


# TODO：价值楼盘
class ValueBuildingView(LoginRequiredMixin, APIView):

    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        value_info = ValueBuilding.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = ValueBuilding.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = ValueBuildingListSerializers(value_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        form = ValueBuildingForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                ValueBuilding.objects.create(
                    city=data['city'],
                    area=data['area'],
                    project_name=data['project_name'],
                    location=data['location'],
                    total_building_area=data['total_building_area'],
                    land_area=data['land_area'],
                    selling_tao=data['selling_tao'],
                    total_tao=data['total_tao'],
                    plot_ratio=data['plot_ratio'],
                    yitui_tao=data['yitui_tao'],
                    in_average=data['in_average'],
                    selling_average=data['selling_average'],
                    product_composition=data['product_composition'],
                    h_area=data['h_area'],
                    supporting_business=data['supporting_business'],
                    supporting_education=data['supporting_education'],
                    traffic_conditions=data['traffic_conditions'],
                    developers=data['developers'],
                    sales=data['sales'],
                    first_time=data['first_time'],

                )
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})
    def put(self, request):
        v_id = request.data.get('id')
        value = ValueBuilding.objects.filter(id=v_id).first()
        form = ValueBuildingForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                value.city = data['city'],
                value.area = data['area'],
                value.project_name = data['project_name']
                value.location = data['location']
                value.total_building_area = data['total_building_area']
                value.land_area = data['land_area']
                value.selling_tao = data['selling_tao']
                value.total_tao = data['total_tao']
                value.plot_ratio = data['plot_ratio']
                value.yitui_tao = data['yitui_tao']
                value.in_average = data['in_average']
                value.selling_average = data['selling_average']
                value.product_composition = data['product_composition']
                value.h_area = data['h_area']
                value.supporting_business = data['supporting_business']
                value.supporting_education = data['supporting_education']
                value.traffic_conditions = data['traffic_conditions']
                value.developers = data['developers']
                value.sales = data['sales']
                value.first_time = data['first_time']
                value.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class ValueBuildingIdView(LoginRequiredMixin, APIView):
    def get(self, request):
        v_id = request.GET.get('id', 1)
        if not v_id:
            return Response({'status': '0', 'msg': '无id'})
        value = ValueBuilding.objects.filter(id=v_id)
        seria = ValueBuildingListSerializers(value, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})


# TODO：TOP200
class TopInView(LoginRequiredMixin, APIView):

    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        top_info = Top_In.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = Top_In.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = TopInListSerializers(top_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        form = TopInForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                Top_In.objects.create(
                    city=data['city'],
                    in_time=data['in_time'],
                    company_name=data['company_name'],
                    develop_project=data['develop_project'],
                    new_ranking=data['new_ranking'],
                    headquarters_location=data['headquarters_location'],
                )
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})
    def put(self, request):
        top_id = request.data.get('id')
        top = Top_In.objects.filter(id=top_id).first()
        form = TopInForm(request.data)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                top.city = data['city']
                top.in_time = data['in_time']
                top.company_name = data['company_name']
                top.develop_project = data['develop_project']
                top.new_ranking = data['new_ranking']
                top.headquarters_location = data['headquarters_location']
                top.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class TopInIdView(LoginRequiredMixin, APIView):
    def get(self, request):
        t_id = request.GET.get('id', 38)
        if not t_id:
            return Response({'status': '0', 'msg': '无id'})
        top = Top_In.objects.filter(id=t_id)
        seria = TopInListSerializers(top, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})


# TODO：大数据
class BigDataView(LoginRequiredMixin, APIView):

    def get(self, request):
        page = int(request.GET.get('page', 1))
        create_on = request.GET.get('create_on')
        condition = {}
        if create_on:
            condition['create_on'] = create_on
        big_info = BigData.objects.filter(**condition).order_by('-id')[(page - 1) * 8:(page - 1) * 8 + 8]
        count = BigData.objects.filter(**condition).count()
        total_page = math.ceil(count / 8)
        if total_page == 0:
            total_page = 1
        seria = BigDataListSerializers(big_info, many=True)
        return Response({'data': seria.data, 'msg': '成功', 'status': '1', 'total_page': total_page})

    def post(self, request):
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        form = BigDataForm(request.data)
        if suffix:
            file_url = Parsing(file_base, suffix)
        else:
            file_url = None
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                BigData.objects.create(
                    city=data['city'],
                    positioning=data['positioning'],
                    city_card=data['city_card'],
                    GDP=data['GDP'],
                    peo_num=data['peo_num'],
                    pillar_industries=data['pillar_industries'],
                    key_enterprises=data['key_enterprises'],
                    development_plan=data['development_plan'],
                    planning_for=data['planning_for'],
                    file_url=file_url
                )
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})

    def put(self, request):
        b_id = request.data.get('id')
        big = BigData.objects.filter(id=b_id).first()
        file_base = request.data.get('file_base')
        suffix = request.data.get('suffix')
        file_url = request.data.get('file_url')
        form = BigDataForm(request.data)
        if suffix:
            file_url = Parsing(file_base, suffix)
        else:
            file_url = file_url
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                big.city = data['city'],
                big.positioning = data['positioning'],
                big.city_card = data['city_card'],
                big.GDP = data['GDP'],
                big.peo_num = data['peo_num'],
                big.pillar_industries = data['pillar_industries'],
                big.key_enterprises = data['key_enterprises'],
                big.development_plan = data['development_plan'],
                big.planning_for = data['planning_for'],
                big.file_url = file_url
                big.save()
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功'})
        return Response({'status': '0', 'msg': '数据不完整'})


class BigDataIdView(LoginRequiredMixin, APIView):
    def get(self, request):
        b_id = request.GET.get('id', 38)
        if not b_id:
            return Response({'status': '0', 'msg': '无id'})
        big = BigData.objects.filter(id=b_id)
        seria = BigDataListSerializers(big, many=True)
        return Response({'status': '1', 'msg': '获取成功', 'data': seria.data})
