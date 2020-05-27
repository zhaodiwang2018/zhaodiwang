# -*- coding: utf-8 -*-
# @Time    : 2019/9/10 15:28
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path
from apps.index.a import *
from apps.index.systemmessage import *
from apps.index.views import *
from apps.index.deleteoeder import DeleteOrderPaying
from apps.index.discern import *
from apps.index.rili import *
from apps.index import views
app_name = 'apps.index'


urlpatterns = [
    path('get_user_name/', GetUserNameView.as_view()),
    # TODO：新建系统消息
    path('create_system_message/', SystemMessageView.as_view()),
    # TODO：获取铃铛值
    path('get_bell/', BellNumber.as_view()),
    # TODO: 获取推送消息和系统消息列表，即全部已读
    path('get_detail/', BellListView.as_view()),
    # TODO:微信jsAPI接口
    # 获取签名
    path('get_token/', TokenView.as_view()),
    # 获取到xml中的数据
    path('get_open/', Atest.as_view()),
    # 微信回调
    path('get_result/', PayResultView.as_view()),
    # TODO:删除预付定单
    path('delete_order_paying/', DeleteOrderPaying.as_view()),
    # 挑刺提交问题 TODO：get（获取挑刺报名的五个问题） post（提交五个问题）
    path('discern/', DiscernView.as_view()),
    # 后端审核 get（列表页）post（审核积分）
    path('audit_question/', DiscernAuditView.as_view()),
    # 判断是否已填写问题
    path('is_ok/', IsOkView.as_view()),
    # 积分记录
    path('int_record/', IntegralRecordView.as_view()),
    # 邀请首页
    path('yq_home/', YaoQingHomePage.as_view()),
    # 邀请注册记录
    path('yaoqing_zc/', YaoQingZhuCeView.as_view()),
    # 内测邀请成功，TODO: 一次性弹窗
    path('is_success/', IsSuccessView.as_view()),
    # 邀请付费
    path('yaoqing_fufei/', YaoQingFFView.as_view()),
    # 积分抵会员
    path('jifen_vip/', JiFenVipView.as_view()),
    # 日历备忘录首页
    path('rili_memo_homepage/', RiLiHomePageView.as_view()),
    # 日历
    path('get_city_list/', CityListView().as_view()),
    # 备忘录
    path('get_memo/', MeMoView.as_view()),
    path('get_memo_list/', MeMoListView.as_view()),
    # 人脉顾问首页
    path('get_renmai/', RenMaiView.as_view()),
    path('get_websokete', views.websocketLink)


]