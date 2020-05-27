# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 9:24
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : smsnotice.py TODO:短信通知
# @Software: PyCharm


from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from rest_framework.views import APIView, Response
from apps.user.models import *
from apps.land.models import *
from apps.land.a import metric
from rest_framework import serializers
from apps.utils.mixin_utils import *
import urllib.parse


# 充值会员 单条发送
class SingleVip(object):
    def __init__(self, mobile, consumption_amount, vip_type):
        self.mobile = mobile
        self.consumption_amount = consumption_amount
        self.vip_type = vip_type
        self.apikey = "31df217fdc515fdd2d53f48171917245"

    def one(self):
        client = YunpianClient(apikey=self.apikey)
        # TODO: 单发
        # 初始化client, apikey作为所有请求的默认值
        tpl_value = urllib.parse.urlencode({'#vip_type#': self.vip_type, '#consumption_amount#': self.consumption_amount})   # 注意此处不要用sdk中的解码方法，超级傻逼
        # code 和 app是你模版里面的变量，我们使用py3的urllib.parse.urlencode方法对此参数进行转码，注意在｛｝中，需要在模版变量前后加上#，不然会返回参数不正确
        param = {YC.MOBILE: self.mobile, YC.TPL_ID: '3256576', YC.TPL_VALUE: tpl_value}
        r = client.sms().tpl_single_send(param)
        # print(r.msg())

        return r.msg()


# 完善信息群发
class InfoBatch(object):
    def __init__(self, mobile):
        self.mobile = mobile

        self.apikey = "31df217fdc515fdd2d53f48171917245"

    def multiple(self):
        client = YunpianClient(apikey=self.apikey)
        # 初始化client, apikey作为所有请求的默认值
        tpl_value = urllib.parse.urlencode({})   # 注意此处不要用sdk中的解码方法，超级傻逼
        # code 和 app是你模版里面的变量，我们使用py3的urllib.parse.urlencode方法对此参数进行转码，注意在｛｝中，需要在模版变量前后加上#，不然会返回参数不正确
        param = {YC.MOBILE: self.mobile, YC.TPL_ID: '3275708', YC.TPL_VALUE: tpl_value}
        r = client.sms().tpl_batch_send(param)
        # print(r.data())
        return r.data()
# mobile = '15037822850,15572525031'
# s_vip = InfoBatch(mobile)
# print(s_vip.multiple())
#
# class PerfectInfoView(APIView):
#     def get(self,request):
#         users = Users.objects.filter(city='[]')
#         mobile_list = []
#         for user in users:
#             mobile_list.append(user.mobile)
#         mobiles = ','.join(str(n) for n in mobile_list)
#         s_vip = InfoBatch(mobiles)
#         print(s_vip.multiple())
#         return Response({'msg': '发送成功', 'status': '1'})