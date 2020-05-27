# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 16:02
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : apppay.py
# @Software: PyCharm


from rest_framework.views import APIView
from apps.utils.alipay import AliPay
from apps.utils.app_pay import AliAppPay
from zhaodi.settings import ali_pub_key_path, private_key_path, ALI_APP_ID
from rest_framework.response import Response
from apps.user.serializers import *
from apps.user.models import *
from apps.land.models import *
from apps.index.models import *
from django.shortcuts import redirect, reverse
from apps.utils.mixin_utils import LoginRequiredMixin

import datetime, pytz
import time
import random


class AliAppPayView(APIView):

    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop("sign", None)
        alipay = AliAppPay(
            app_id=ALI_APP_ID,
            notify_url="http://118.31.60.22:8000/user/ali_app_pay/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://118.31.60.22:8000/user/ali_app_pay"
        )

        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            existed_order = OrderInfo.objects.filter(order_sn=order_sn).first()
            try:
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.datetime.now()
                existed_order.save()
                response = redirect(reverse('apps.user:index2'))
                # response.set_cookie("nextPath", "pay", max_age=3)
                return response
            except:
                response = redirect('apps.user:index2')
                return response
        else:
            response = redirect('apps.user:index2')
            return response

    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop("sign", None)
        alipay = AliAppPay(
            app_id=ALI_APP_ID,
            notify_url="http://118.31.60.22:8000/user/ali_app_pay/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://118.31.60.22:8000/user/ali_app_pay/"
        )
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)
            existed_order = OrderInfo.objects.filter(order_sn=order_sn).first()
            existed_order.trade_no = trade_no
            existed_order.pay_time = datetime.datetime.now()
            existed_order.pay_status = trade_status
            # 判断是充值会员
            if existed_order.subject in ['年', '季','月','双周']:
                if existed_order.subject == '年':
                    days = 365
                    vip_num = 4
                elif existed_order.subject == '季':
                    days = 90
                    vip_num = 3
                elif existed_order.subject == '月':
                    days = 30
                    vip_num = 2
                elif existed_order.subject == '双周':
                    days = 14
                    vip_num = 1
                else:
                    days = 0
                    vip_num = 0
                vip = VipExpire.objects.filter(user_id=existed_order.user_id).first()
                user = Users.objects.filter(id=existed_order.user_id).first()
                # 是否vip
                if vip:
                    # 如果没到期
                    if vip.expire_time.replace(tzinfo=pytz.timezone('UTC')) > datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')):
                        vip.expire_time = vip.expire_time.replace(tzinfo=pytz.timezone('UTC')) + datetime.timedelta(days=days)
                        vip.save()
                    else:
                        vip.expire_time = existed_order.pay_time.replace(tzinfo=pytz.timezone('UTC')) + datetime.timedelta(days=days)
                        vip.save()
                    if user.vip_num <= vip_num:
                        user.vip_num = vip_num
                        user.save()
                    else:
                        user.vip_num = user.vip_num
                else:
                    VipExpire.objects.create(user_id=existed_order.user_id,expire_time=existed_order.pay_time.replace(tzinfo=pytz.timezone('UTC')) + datetime.timedelta(days=days))
                    user.vip_num = vip_num
                    user.save()
                if existed_order.subject == '月':
                    give_jifen = 368
                elif existed_order.subject == '季':
                    give_jifen = 1198
                elif existed_order.subject == '年':
                    give_jifen = 5988
                else:
                    give_jifen = 0
                user.integration += give_jifen
                user.save()
                IntegralRecord.objects.create(integral_type='开通' + existed_order.subject + '度超级VIP', integral=give_jifen, user_id=existed_order.user_id)
                content = '恭喜您获得超级' + existed_order.subject + '度VIP特权，全场土地信息任意看，本月沙龙、月报会免费报名，榜单和数据无限下载。本次消费金额'\
                          + str(existed_order.order_mount) + '元，额外获得' + str(give_jifen) + '积分。'
                system_notice = SystemMessageModel.objects.filter(trade_no=existed_order.trade_no).first()
                if not system_notice:
                    try:
                        SystemMessageModel.objects.create(content=content, sys_type='会员充值', user_id=existed_order.user_id, trade_no=existed_order.trade_no)
                    except:
                        return Response({'msg': '系统消息创建失败', 'status': '0'})
            else:
                fabu = ReleaseRecord.objects.filter(land_id=existed_order.land_id, luyou=existed_order.luyou).first()
                if not Contact.objects.filter(user_id=existed_order.user_id, land_id=existed_order.land_id,
                                              contacted_id=fabu.user_id, luyou=existed_order.luyou):
                    Contact.objects.create(user_id=existed_order.user_id, land_id=existed_order.land_id,
                                           contacted_id=fabu.user_id, luyou=existed_order.luyou)
                user = Users.objects.filter(id=existed_order.user_id).first()
                content = '恭喜您成功购买' + existed_order.subject + '，消费' + str(existed_order.order_mount) + '元'
                # if existed_order.luyou == '/tudimessage/zhuanrang':
                    # TODO:退款
                contented = '恭喜您,您的' + existed_order.subject + '订单，已被' + user.username + '购买'
                system_notice = SystemMessageModel.objects.filter(trade_no=existed_order.trade_no).first()
                if not system_notice:
                    SystemMessageModel.objects.create(content=contented, sys_type='售出信息', user_id=fabu.user_id,
                                                      trade_no=existed_order.trade_no)
                    SystemMessageModel.objects.create(content=content, sys_type='购买信息', user_id=existed_order.user_id,
                                                      trade_no=existed_order.trade_no)

            existed_order.save()
            today = datetime.date.today()
            today_data = AdminUserChart.objects.filter(create_on=today).first()
            if today_data:
                today_data.today_fufei += existed_order.order_mount
                today_data.save()
            else:
                user_num = Users.objects.count()
                AdminUserChart.objects.create(today_fufei=existed_order.order_mount, user_all=user_num)
            return Response("success")


class AppPayView(APIView):
    def get_is_pay(self, luyou, land_id, user_id):
        return OrderInfo.objects.filter(user_id=user_id, luyou=luyou, land_id=land_id, pay_status='TRADE_SUCCESS').first()

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = Users.objects.filter(id=user_id).first()
        land_id = request.GET.get('land_id')
        luyou = request.GET.get('luyou')
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=user_id, ranstr=random.randint(10, 99))
        pay = self.get_is_pay(luyou, land_id, user_id)
        if pay:
            return Response({'msg': '该订单已支付', 'status': '0'})
        if luyou == '/tudimessage/nitui' or luyou == '/tudimessage/paimai' or luyou == '/tudimessage/guapai' or luyou == '/tudimessage/xiancheng':
            land = LandInfo.objects.filter(id=land_id).first()
            reward_price = land.reward_price
            title = land.title

        elif luyou == '/tudimessage/zhaoshang':
            land = AttractInfo.objects.filter(id=land_id).first()
            reward_price = land.reward_price
            title = land.title

        elif luyou == '/tudimessage/zhuanrang':
            land = TransInfo.objects.filter(id=land_id).first()
            reward_price = land.reward_price
            title = land.title

        elif luyou == '/activity/shalong' or luyou == '/activity/yuebao' or luyou == '/activity/tuijie' or luyou == '/activity/kuanian':
            land = Activity.objects.filter(id=land_id).first()
            reward_price = land.reward_price
            title = land.title

        elif luyou == "/tudilist/nadi" or luyou == "/tudilist/gongdi" or luyou == "/tudilist/shoulou" or luyou == "/tudilist/loupan":
            land = PropertyList.objects.filter(id=land_id).first()
            reward_price = land.reward_price
            title = land.title

        elif luyou == "/Investment/zhoubao" or luyou == "/Investment/yuebao" or luyou == "/Investment/jibao" or luyou == "/Investment/bannnianbao" or luyou == "/Investment/nianbao":
            land = InvestmentData.objects.filter(id=land_id).first()
            reward_price = land.reward_price
            title = land.title
        elif luyou == 'userinfo2':
            vip_type = request.GET.get('vip_type', '年')
            if vip_type == '年':
                reward_price = 12988
            elif vip_type == '季':
                reward_price = 3568
            elif vip_type == '月':
                reward_price = 1298
            elif vip_type == '双周':
                reward_price = 0.01
            else:
                return Response({'status': '0'})
            alipay = AliAppPay(
                app_id=ALI_APP_ID,
                notify_url="http://118.31.60.22:8000/user/ali_app_pay/",
                app_private_key_path=private_key_path,
                alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                debug=True,  # 默认False,
                return_url="http://118.31.60.22:8000/user/ali_app_pay"
            )
            url = alipay.direct_pay(
                subject=vip_type + '会员',
                out_trade_no=order_sn,
                total_amount=reward_price,
                return_url="http://118.31.60.22:8000/user/ali_app_pay"
            )
            OrderInfo.objects.create(user_id=user_id, order_mount=reward_price, order_sn=order_sn, subject=vip_type,
                                    luyou=luyou, order_type=2)
            # re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
            re_url = "https://openapi.alipay.com/gateway.do?{data}".format(data=url)
            return Response({'re_url': re_url, 'msg': '成功', 'status': '1'})
        else:
            return Response({'msg': '路由错了'})

        alipay = AliAppPay(
            app_id=ALI_APP_ID,
            notify_url="http://118.31.60.22:8000/user/ali_app_pay/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=False,  # 默认False,
            return_url="http://118.31.60.22:8000/user/ali_app_pay"
        )
        url = alipay.direct_pay(
            subject=title,
            out_trade_no=order_sn,
            total_amount=reward_price,
            return_url="http://118.31.60.22:8000/user/ali_app_pay"
        )
        OrderInfo.objects.create(user_id=user_id, order_mount=reward_price, order_sn=order_sn, subject=title, land_id=land_id, luyou=luyou)
        # re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        re_url = "https://openapi.alipay.com/gateway.do?{data}".format(data=url)
        return Response({'re_url': re_url, 'msg': '成功', 'status': '1'})