from django.urls import path

from django.urls import path
from apps.land.upimg import *
from apps.land.clientland import *
from apps.land.dataentry import *
from apps.land.selfcenter import *
from apps.land.audit import *
from apps.land.cliententry import *
from apps.land.homepage import *
from apps.land.delivery import *
from apps.land.views import *
from apps.land.mobileself import *

app_name = 'apps.land'

urlpatterns = [
    # 首页
    path('home/', HomePageView.as_view()),
    path('hot_top/', HotTop.as_view()),
    path('a/', A.as_view()),
    # 收藏
    path('collection/', CollectionView.as_view()),
    # 个人中心表格
    path('selftable/', SelfTableView.as_view()),
    # 个人中心数据统计
    path('self_num/', SelfNumber.as_view()),
    # 手机端个人中心（TODO:三个数字）
    path('mobile_self/', MobileSelf.as_view()),
    # 记录
    path('record/', RecordView.as_view()),
    # pc资讯列表
    path('land_list/', LandView.as_view()),
    # mobile资讯列表
    # path('land_mobile_list/', MobileLandView.as_view()),
    # 资讯详情
    path('land_detail/', LandDetailView.as_view()),
    # 富文本上传图片
    path('up_img/', UpImag.as_view()),
    # 前端新建公告 TODO：get：获取详情，post：新建公告信息，put: 修改公告
    path('create_client_notice/', LandUpView.as_view()),
    # 前端新建转让 TODO：get：获取详情，post：新建转让信息，put: 修改转让
    path('create_client_trans/', TransUpView.as_view()),
    # 前端新建招商 TODO：get：获取详情，post：新建招商信息，put: 修改招商
    path('create_client_attract/', AttractUpView.as_view()),
    # 活动详情  TODO：get：获取详情， post：新建活动信息， put：修改活动信息
    path('create_client_activity/', ActivityInfoView.as_view()),
    # 榜单详情  TODO：get：获取详情， post：新建榜单信息， put：修改榜单信息
    path('create_client_poplist/', PropertyListView.as_view()),
    # 投资数据详情  TODO：get：获取详情， post：新建投资数据信息， put：修改投资数据信息
    path('create_client_inv/', InvestmentDataView.as_view()),
    # 土地信息列表
    path('get_lands/', LandDataListView.as_view()),
    # 公告列表 TODO：get：列表，post：下架
    path('get_notice_list/', NoticeEntryView.as_view()),
    # 转让列表 TODO：get：列表，post：下架
    path('get_trans_list/', TransEntryView.as_view()),
    # 招商列表 TODO：get：列表，post：下架
    path('get_attract_list/', AttractEntryView.as_view()),
    # 活动列表 TODO：get：列表，post：下架
    path('get_activity_list/', ActivityDeleteView.as_view()),
    # 榜单列表 TODO：get：列表，post：下架
    path('get_pop_list/', PopListDeleteView.as_view()),
    # 投资数据列表 TODO：get：列表，post：下架
    path('get_inv_list/', InvestmentDataDeleteView.as_view()),
    # 成交列表
    path('get_deal_list/', DealView.as_view()),
    # 录入成交
    path('create_deal/', DealView.as_view()),
    # 获取成交id
    path('get_deal_id/', DealIdView.as_view()),
    # 收并购列表
    path('get_chargemerge_list/', InvChargeMergeView.as_view()),
    # 录入收并购
    path('create_chargemerge/', InvChargeMergeView.as_view()),
    # 编辑收并购
    path('update_chargemerge/', InvChargeMergeView.as_view()),
    # 获取收并购id
    path('get_chargemerge_id/', InvChargeMergeIdView.as_view()),
    # 楼市供应列表
    path('get_supply_list/', BuildingSupplyFView.as_view()),
    # 录入楼市供应
    path('create_supply/', BuildingSupplyFView.as_view()),
    # 编辑楼市供应
    path('update_supply/', BuildingSupplyFView.as_view()),
    # 楼市供应id
    path('get_supply_id/', BuildingSupplyFIdView.as_view()),
    # 楼市成交列表
    path('get_supply_deal_list/', BuildingSupplyTView.as_view()),
    # 录入楼市成交
    path('create_supply_deal/', BuildingSupplyTView.as_view()),
    # 编辑楼市成交
    path('update_supply_deal/', BuildingSupplyTView.as_view()),
    # 楼市成交id
    path('get_supply_deal_id/', BuildingSupplyTIdView.as_view()),
    # 价值楼盘列表
    path('get_value_list/', ValueBuildingView.as_view()),
    # 录入价值楼盘
    path('create_value/', ValueBuildingView.as_view()),
    # 编辑价值楼盘
    path('update_value/', ValueBuildingView.as_view()),
    # 价值楼盘id
    path('get_value_id/', ValueBuildingIdView.as_view()),
    # top200列表
    path('get_top_list/', TopInView.as_view()),
    # 录入top200进驻
    path('create_top/', TopInView.as_view()),
    # 编辑top200进驻
    path('update_top/', TopInView.as_view()),
    # top200 id
    path('get_top_id/', TopInIdView.as_view()),
    # 大数据列表
    path('get_big_data_list/', BigDataView.as_view()),
    # 录入大数据
    path('create_big_data/', BigDataView.as_view()),
    # 编辑大数据
    path('update_big_data/', BigDataView.as_view()),
    # 大数据id
    path('get_big_data_id/', BigDataIdView.as_view()),
    # 发布记录
    path('get_release/', ReleaseRecordDetailView.as_view()),
    # 公告审核
    path('get_land_audit/', AuditLandView.as_view()),
    # 转让审核
    path('get_trans_audit/', AuditTransView.as_view()),
    # 招商审核
    path('get_attract_audit/', AuditAttractView.as_view()),
    # 活动审核
    path('get_activity_audit/', AuditActivityView.as_view()),
    # 榜单审核
    path('get_pop_audit/', AuditPopListView.as_view()),
    # 投资数据审核
    path('get_investment_audit/', AuditInvestmentView.as_view()),
    # 获取邀请详情
    path('get_yaoqing/', YaoqingDetailView.as_view()),
    # 交付页面
    path('delivery/', DeliveryLandView.as_view()),
    # 给坐标
    path('get_zuobiao/', CoordinatesView.as_view()),
    # 手机端个人中心四个数字（取第一个）
    path('mse/', Mse.as_view()),

    #




]
