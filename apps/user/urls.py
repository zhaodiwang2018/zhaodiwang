from django.urls import path
from apps.user.views import *
from apps.user.enditdata import *
from apps.user.orderpay import *
from apps.user.apppay import *
from django.views.generic import TemplateView
from apps.user.userlist import *
from apps.user.clock import *
from apps.user.ranking import *

app_name = 'apps.user'

urlpatterns = [
    # 验证手机号
    path('verify_mobile/', VerifyMobileView.as_view()),
    # 发送验证码
    path('send_code/', SmsCodeView.as_view()),
    # 注册
    path('register/', RegisterView.as_view()),
    # 忘记密码验证码
    path('forget_password_verify/', ForgetPasswordView.as_view()),
    # 修改密码
    path('update_password/', ForgetPasswordView.as_view()),
    # 登录
    path('login/', LoginView.as_view()),
    # admin登录
    path('admin_login/', AdminLoginView.as_view()),
    # 个人编辑
    path('edit/', SelfEditView.as_view()),
    path('ali_pay/', AliPayView.as_view()),
    path('ali_app_pay/', AliAppPayView.as_view()),
    path('app_pay/', AppPayView.as_view()),
    # TODO:get(支付)，post（模拟支付）
    path('pay/', PayView.as_view()),
    path('index/', TemplateView.as_view(template_name='test.html'), name='index'),
    path('index2/', TemplateView.as_view(template_name='test2.html'), name='index2'),
    path('order_list/', OrderListView.as_view()),
    # vip
    path('vip_pay/', VipPayView.as_view()),
    # TODO:后端用户列表
    path('user_list/', UserListView.as_view()),
    # TODO：打卡 get（用户今日是否已打卡） post（打卡，并提交一个问题）put（用户个人打卡记录）
    path('clock/', ClockView.as_view()),
    # 更新用户中心数据
    path('update_data/', UpdateDataView.as_view()),
    # 排行榜列表
    path('act_list/', RankingListView.as_view()),
    # 发短信
    # path('send_p/', PerfectInfoView.as_view()),
    # test
    path('data_sta/', DataStatistics.as_view()),

]