# from yunpian_python_sdk.model import constant as YC
# from yunpian_python_sdk.ypclient import YunpianClient
# import urllib.parse
#
#
# class SingleVip(object):
#     def __init__(self, mobile, consumption_amount, vip_type):
#         self.mobile = mobile
#         self.consumption_amount = consumption_amount
#         self.type = type
#         self.apikey = "31df217fdc515fdd2d53f48171917245"
#
#     def one(self):
#         client = YunpianClient(apikey='31df217fdc515fdd2d53f48171917245')
#         # TODO: 单发
#         # 初始化client, apikey作为所有请求的默认值
#         tpl_value = urllib.parse.urlencode({'#type#': self.type, '#content#': self.consumption_amount})   # 注意此处不要用sdk中的解码方法，超级傻逼
#         # code 和 app是你模版里面的变量，我们使用py3的urllib.parse.urlencode方法对此参数进行转码，注意在｛｝中，需要在模版变量前后加上#，不然会返回参数不正确
#         param = {YC.MOBILE: self.mobile, YC.TPL_ID: '3256576', YC.TPL_VALUE: tpl_value}
#         r = client.sms().tpl_single_send(param)
#         print(r.msg())
#
# a = '1qw'
# s = a.isdigit()
# print(s)
import operator
a = [{'a': '2'}, {'a': '4'}, {'a': '1'}, {'a': '6'}]
b = sorted(a, key=operator.itemgetter('a'))

print(b.index({'a': '1'}))
# del a['a']
# print(a)
# a = [1, 2]
# a.remove(1)
# print
# import datetime
# a = datetime.datetime.now()
# print(str(a))