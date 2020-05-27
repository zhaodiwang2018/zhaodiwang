from rest_framework.views import APIView, Response
from apps.index.models import *
from apps.user.models import *
from apps.land.models import *
from django.core.cache import cache
from apps.utils.mixin_utils import *
from xml.etree import ElementTree
from urllib import parse
from apps.utils.parsing import Parsing
from apps.user.smsnotice import *
import string
import random
import requests
import time
import hashlib
import datetime
import pytz
import os

# Create your views here.


secret = '1e75e41c1ffca1868670050c8acd5fb0'
WECHAT_APPID = 'wxa546a4615ba1e489'
body = 'JSAPI支付测试'
WECHAT_MCH_ID = '1551385521'
WECHAT_PAY_NOTIFY_URL = 'http://118.31.60.22:8000/notice/get_result/'
spbill_create_ip = '118.31.60.22'
wechat_openid = 'oJ5ssxO9Nn6Qa6Dt1bhgVlJ7tYgQ'
trade_type = 'JSAPI'
WECHAT_PAY_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A'
chars = string.ascii_letters + string.digits


# 获取access_token
def accesstokens():
    access_token = cache.get('access_token')
    if access_token:
        return access_token
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + WECHAT_APPID + "&secret=" + secret

    res = requests.get(url).json()
    access_token = str(res['access_token'])
    cache.set("access_token", access_token, 7200)
    return access_token


# 获取微信JsApiTicket
def getJsApiTicket():
    jsapi_ticket = cache.get('jsapi_ticket')
    if jsapi_ticket:
        return jsapi_ticket
    accessToken = accesstokens()
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=' + accessToken + "&type=jsapi"
    res = requests.get(url).json()
    jsapi_ticket = str(res['ticket'])
    cache.set('jsapi_ticket', jsapi_ticket, 7200)
    return jsapi_ticket


# 创建16位nonce_str
def createNonceStr():
    import random
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    nonce_str = ""
    for i in range(0, 16):
        s = random.randint(0, len(chars) - 1)
        nonce_str += chars[s:s + 1]
    return nonce_str


#
class TokenView(APIView):

    def post(self, request):
        jsapiTicket = getJsApiTicket()
        timestamp = int(time.time())
        noncestr = createNonceStr()
        url_quo = request.data.get('url')

        url = parse.unquote(url_quo)
        ret = {
            'noncestr': noncestr,
            'jsapi_ticket': jsapiTicket,
            'timestamp': timestamp,
            'url': url,
        }
        string = '&'.join(
            ['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)]
        )
        sha1 = hashlib.sha1()
        sha1.update(string.encode('utf-8'))
        signature = sha1.hexdigest()
        package = {

            'app_id': WECHAT_APPID,
            'noncestr': noncestr,
            'timestamp': timestamp,
            'signature': signature
        }

        return Response(package)


class Atest(APIView):
    def get(self, request):
        out_trade_no = request.GET.get('out_trade_no')

        res = OrderInfo.objects.filter(order_sn=out_trade_no, pay_status='TRADE_SUCCESS').first()
        if res:
            pay = True
        else:
            pay = False
        return Response({'data': pay})

    def post(self, request):
        user_id = request.data.get('user_id')
        land_id = request.data.get('land_id')
        luyou = request.data.get('luyou')
        out_trade_no = request.data.get('out_trade_no')
        if luyou == '/tudimessage/nitui' or luyou == '/tudimessage/paimai' or luyou == '/tudimessage/guapai' or luyou == '/tudimessage/xiancheng':
            land = LandInfo.objects.filter(id=land_id).first()
            reward_price = int(land.reward_price * 100)
            title = land.title

        elif luyou == '/tudimessage/zhaoshang':
            land = AttractInfo.objects.filter(id=land_id).first()
            reward_price = int(land.reward_price * 100)
            title = land.title

        elif luyou == '/tudimessage/zhuanrang':
            land = TransInfo.objects.filter(id=land_id).first()
            reward_price = int(land.reward_price * 100)
            title = land.title

        elif luyou == '/activity/shalong' or luyou == '/activity/yuebao' or luyou == '/activity/tuijie' or luyou == '/activity/kuanian':
            land = Activity.objects.filter(id=land_id).first()
            reward_price = int(land.reward_price * 100)
            title = land.title

        elif luyou == "/tudilist/nadi" or luyou == "/tudilist/gongdi" or luyou == "/tudilist/shoulou" or luyou == "/tudilist/loupan":
            land = PropertyList.objects.filter(id=land_id).first()
            reward_price = int(land.reward_price * 100)
            title = land.title

        elif luyou == "/Investment/zhoubao" or luyou == "/Investment/yuebao" or luyou == "/Investment/jibao" or luyou == "/Investment/bannnianbao" or luyou == "/Investment/nianbao":
            land = InvestmentData.objects.filter(id=land_id).first()
            reward_price = int(land.reward_price * 100)
            title = land.title
        elif luyou == "userinfo2":
            if land_id == '年':
                reward_price = int(12988 * 100)
                title = land_id
            elif land_id == '季':
                reward_price = int(3568 * 100)
                title = land_id

            elif land_id == '月':
                reward_price = int(1298 * 100)
                title = land_id

            else:
                return Response({'status': '0'})
        else:
            return Response({'msg': '路由错了'})
        code = request.data.get('code')
        code = code.split('&')[0].split('=')[1]
        nonce_str = ''.join([random.choice(chars) for i in range(32)])  # 随机字符串，不长于32位。 ok
        wechat_openid = requests.get(
            'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(
                WECHAT_APPID, secret, code))
        stringA = "appid={}&body={}&mch_id={}&nonce_str={}&notify_url={}&openid={}&out_trade_no={}&spbill_create_ip={}&total_fee={}&trade_type={}&key={}".format(
            WECHAT_APPID, title, WECHAT_MCH_ID, nonce_str, WECHAT_PAY_NOTIFY_URL, wechat_openid.json()['openid'],
            out_trade_no,
            spbill_create_ip, str(reward_price), trade_type, WECHAT_PAY_KEY)
        m2 = hashlib.md5()
        m2.update(stringA.encode('utf-8'))
        sign = m2.hexdigest().upper()
        xml = """
        <xml>
            <appid>""" + WECHAT_APPID + """</appid>
            <body>""" + title + """</body>
            <mch_id>""" + WECHAT_MCH_ID + """</mch_id>
            <nonce_str>""" + nonce_str + """</nonce_str>
            <notify_url>""" + WECHAT_PAY_NOTIFY_URL + """</notify_url>
            <openid>""" + wechat_openid.json()['openid'] + """</openid>
            <out_trade_no>""" + out_trade_no + """</out_trade_no>
            <spbill_create_ip>118.31.60.22</spbill_create_ip>
            <total_fee>""" + str(reward_price) + """</total_fee>
            <trade_type>""" + trade_type + """</trade_type>
            <sign>""" + sign + """</sign>
        </xml>
        """
        r = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml.encode('utf-8'))
        root = ElementTree.fromstring(r.content)
        if root.find('return_code').text == 'SUCCESS' and root.find('result_code').text == 'SUCCESS':
            timeStamp = str(time.time())[:10]
            nonceStr = root.find('nonce_str').text
            packagestr = 'prepay_id=' + root.find('prepay_id').text
            stringB = "appId=" + WECHAT_APPID + "&nonceStr=" + nonceStr + "&package=" + packagestr + "&signType=MD5" + "&timeStamp=" + timeStamp + "&key=" + WECHAT_PAY_KEY
            m2 = hashlib.md5()
            m2.update(stringB.encode('utf-8'))
            sign = m2.hexdigest().upper()
            if land_id in ['年', '季', '月']:
                OrderInfo.objects.create(user_id=user_id, order_mount=reward_price / 100, order_sn=out_trade_no,
                                         subject=title, luyou=luyou, order_type=2)
            else:
                OrderInfo.objects.create(user_id=user_id, order_mount=reward_price / 100, order_sn=out_trade_no,
                                         subject=title,
                                         land_id=land_id, luyou=luyou, order_type=2)
            return Response(
                {'result': '1',
                 'data': {'timeStamp': timeStamp, 'nonceStr': nonceStr, 'paySign': sign, 'package': packagestr,
                          'signType': 'MD5'}})
        # return Response({'data':root.find('prepay_id').text})
        else:
            return Response({'result': '0', 'message': root.find('return_msg').text, 'data': {}})


class PayResultView(APIView):
    """post:更新微信支付结果"""

    def post(self, request):
        _xml = request.body
        xml = str(_xml, encoding="utf-8")
        return_dict = {}
        tree = ElementTree.fromstring(xml)
        return_code = tree.find("return_code").text
        if return_code == 'FAIL':
            # 官方发出错误
            return_dict['message'] = '支付失败'
            return Response({'data': return_dict, 'status': '0'})
        elif return_code == 'SUCCESS':
            # 拿到自己这次支付的 out_trade_no
            _out_trade_no = tree.find("out_trade_no").text
            _transaction_id = tree.find("transaction_id").text
            order = OrderInfo.objects.filter(order_sn=_out_trade_no).first()
            order.trade_no = _transaction_id
            order.pay_time = datetime.datetime.now()
            order.pay_status = 'TRADE_SUCCESS'
            user = Users.objects.filter(id=order.user_id).first()

            if order.subject in ['年', '季', '月']:
                if order.subject == '年':
                    days = 365
                    vip_num = 4
                elif order.subject == '季':
                    days = 90
                    vip_num = 3
                elif order.subject == '月':
                    days = 30
                    vip_num = 2
                elif order.subject == '双周':
                    days = 14
                    vip_num = 1
                else:
                    days = 0
                    vip_num = 0
                vip = VipExpire.objects.filter(user_id=order.user_id).first()
                # 是否vip
                if vip:
                    # 如果没到期
                    if vip.expire_time.replace(tzinfo=pytz.timezone('UTC')) > datetime.datetime.now().replace(
                            tzinfo=pytz.timezone('UTC')):
                        vip.expire_time = vip.expire_time.replace(tzinfo=pytz.timezone('UTC')) + datetime.timedelta(
                            days=days)
                        vip.save()
                    else:
                        vip.expire_time = order.pay_time.replace(
                            tzinfo=pytz.timezone('UTC')) + datetime.timedelta(days=days)
                        vip.save()
                    if user.vip_num <= vip_num:
                        user.vip_num = vip_num
                        user.save()
                    else:
                        user.vip_num = user.vip_num
                        user.save()
                else:
                    VipExpire.objects.create(user_id=order.user_id, expire_time=order.pay_time.replace(
                        tzinfo=pytz.timezone('UTC')) + datetime.timedelta(days=days))
                    user.vip_num = vip_num
                    user.save()
                if order.subject == '月':
                    give_jifen = 368
                elif order.subject == '季':
                    give_jifen = 1198
                elif order.subject == '年':
                    give_jifen = 5988
                else:
                    give_jifen = 0
                user.integration += give_jifen
                user.save()
                IntegralRecord.objects.create(integral_type='开通' + order.subject + '度超级VIP', integral=give_jifen,
                                              user_id=order.user_id)
                content = '恭喜您获得超级' + order.subject + '度VIP特权，全场土地信息任意看，本月沙龙、月报会免费报名，榜单和数据无限下载。本次消费金额' \
                          + str(order.order_mount) + '元，额外获得' + str(give_jifen) + '积分。'
                system_notice = SystemMessageModel.objects.filter(trade_no=order.trade_no).first()
                # 发送会员通知短信
                # s_vip = SingleVip(user.mobile, str(order.order_mount), order.subject)
                # print(s_vip.one())
                if not system_notice:
                    try:
                        SystemMessageModel.objects.create(content=content, sys_type='会员充值', user_id=order.user_id)
                    except:
                        return Response({'msg': '系统消息创建失败', 'status': '0'})
            else:
                fabu = ReleaseRecord.objects.filter(land_id=order.land_id, luyou=order.luyou).first()
                if not Contact.objects.filter(user_id=order.user_id, land_id=order.land_id,
                                              contacted_id=fabu.user_id, luyou=order.luyou):
                    Contact.objects.create(user_id=order.user_id, land_id=order.land_id,
                                           contacted_id=fabu.user_id, luyou=order.luyou)
                user = Users.objects.filter(id=order.user_id).first()
                content = '恭喜您成功购买' + order.subject + '，消费' + str(order.order_mount) + '元'
                # if order.luyou == '/tudimessage/zhuanrang':
                # TODO:退款
                contented = '恭喜您,您的' + order.subject + '订单，已被' + user.username + '购买'
                system_notice = SystemMessageModel.objects.filter(trade_no=order.trade_no).first()
                if not system_notice:
                    SystemMessageModel.objects.create(content=content, sys_type='购买信息', user_id=order.user_id,
                                                      trade_no=order.trade_no)
                    SystemMessageModel.objects.create(content=contented, sys_type='售出信息', user_id=fabu.user_id,
                                                      trade_no=order.trade_no)
            order.save()
            today = datetime.date.today()
            today_data = AdminUserChart.objects.filter(create_on=today).first()
            if today_data:
                today_data.today_fufei += order.order_mount
                today_data.save()
            else:
                user_num = Users.objects.count()
                AdminUserChart.objects.create(today_fufei=order.order_mount, user_all=user_num)
            if user.usertype == '1' \
                                '':
                user_p = PaiMing.objects.filter(user_id=user.id).first()
                user_p.act_num += order.order_mount * 0.1
                user_p.save()
            h_xml = "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
            return HttpResponse(h_xml)


class YaoQingFFView(APIView):

    def get(self, request):
        yaoqingren_id = int(request.GET.get('yaoqing_zhuce_id'))
        if not yaoqingren_id:
            return Response({'msg': '无yaoqing_zhuce_id', 'status': '0'})
        beiyaoqing_id = int(request.GET.get('beiyaoqing_id'))
        if not beiyaoqing_id:
            return Response({'msg': '无beiyaoqing_id', 'status': '0'})
        if beiyaoqing_id == yaoqingren_id:
            return Response({'msg': '本人邀请， 无效', 'status': '2'})
        vip_type = request.GET.get('vip_type')
        if vip_type == '月':
            give_jifen = 199
        elif vip_type == '季':
            give_jifen = 699
        elif vip_type == '年':
            give_jifen = 2999
        else:
            give_jifen = 0
        # 被邀请人数据处理
        beiyaoqing_user = Users.objects.filter(id=beiyaoqing_id).first()
        beiyaoqing_user.integration += give_jifen
        beiyaoqing_user.y_int += give_jifen
        beiyaoqing_user.save()
        beiyaoqing_content = '恭喜您被邀请成为{}会员，赠送{}积分'.format(vip_type, give_jifen)
        SystemMessageModel.objects.create(content=beiyaoqing_content, sys_type='被邀请会员充值',
                                          user_id=beiyaoqing_id)
        NeiCe.objects.create(user_id=beiyaoqing_id, leibie='邀请')
        IntegralRecord.objects.create(integral_type='被邀请付费获得积分', integral=give_jifen, user_id=beiyaoqing_id)
        if beiyaoqing_user.usertype == '1':
            paiming_b = PaiMing.objects.filter(user_id=beiyaoqing_user.id).first()
            paiming_b.act_num += give_jifen * 0.3
            paiming_b.save()
        # 邀请人数据处理
        yaoqing_user = Users.objects.filter(id=yaoqingren_id).first()
        yaoqing_user.integration += give_jifen
        yaoqing_user.y_int += give_jifen
        yaoqing_user.save()
        yaoqing_content = '恭喜您成功邀请{}成为{}会员，赠送{}积分'.format(beiyaoqing_user.username, vip_type, give_jifen)
        InviteRegister.objects.create(invite_peo_id=int(yaoqingren_id), register_peo_id=int(beiyaoqing_id),
                                      yq_type='邀请付费')
        SystemMessageModel.objects.create(content=yaoqing_content, sys_type='邀请会员充值',
                                          user_id=yaoqingren_id)
        IntegralRecord.objects.create(integral_type='邀请付费获得积分', integral=give_jifen, user_id=yaoqingren_id)
        if yaoqing_user.usertype == '1':
            paiming_y = PaiMing.objects.filter(user_id=yaoqing_user.id).first()
            paiming_y.act_num += give_jifen * 0.3
            paiming_y.save()
        return Response({'msg': '成功', 'status': '1'})


# from dwebsocket.decorators import accept_websocket,require_websocket
# import json
# # a = {
# #     'name' : 'ACME',
# #     'shares' : 100,
# #     'price' : 542.23
# # }
# # print(json.dumps(a))
# @accept_websocket
# def test_websocket(request):
#     global a
#     print(request.is_websocket())
#     if request.is_websocket():
#
#         for message in request.websocket:
#             print(type(message))
#             a += str(message)
#             print(a)
#             request.websocket.send(a)
#             print(message)
#             print(request.websocket.count_messages())
#             if request.websocket.has_messages():
#                 print(request.websocket.wait())
#         while 1:
#             time.sleep(1) ## 向前端发送时间
#             dit = {
#                 'time':time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
#             }
#             request.websocket.send(json.dumps(dit))
# else:
#     request.websocket.send('111')
# request.websocket.send('222')

# return HttpResponse({'0':1})


import threading
import json
from dwebsocket.decorators import accept_websocket

# 存储连接websocket的用户池
clients = {}
cli_list = []
img_list = []
print(clients,cli_list)

# 记录连接人数   其实没什么卵用  = =


# 连接websocket  ws://localhost：8000/websocketLink/22
# 因为 websocket 是协议  所以不能用 http或https
@accept_websocket
def websocketLink(request):
    user_id = int(request.GET.get('id'))
    user = Users.objects.filter(id=user_id).first()
    # 连接websocket
    global count
    # 获取连接
    if request.is_websocket:
        if user_id not in cli_list:
            cli_list.append(user_id)
            # if not img_list:
            #     img_list.append({'user_id': user_id, 'time_str': str(datetime.datetime.now()), 'img': user.img,
            #                      'username': user.username, })
            # result = filter(lambda x: x['user_id'] == user_id, img_list)
            # if len(list(result)) == 0:
            #     img_list.append({'user_id': user_id, 'time_str': str(datetime.datetime.now()), 'img': user.img,
            #                      'username': user.username, })
        # lock = threading.RLock()  # rlock线程锁
        try:
            # lock.acquire()  # 抢占资源
            # 更新存储用户连接池
            clients[user_id] = request.websocket
            # TODO:如果有接收到的未读消息，则像自己发送其他人的列表
            cus_user = UserListModel.objects.filter(customer_id=user_id).first()
            if cus_user:
                clients[user_id].send(json.dumps({'code': 200, 'y_list': eval(cus_user.y_list)}))
            # TODO:给双方历史记录
            all_history = HistoryRecord.objects.all()
            h_dict = {}
            for his in all_history:
                if user_id in eval(his.bond):
                    for b_id in eval(his.bond):
                        if b_id != user_id:
                            h_dict[str(b_id)] = eval(his.record)
            # 给自己发送历史纪录
            clients[user_id].send(json.dumps({'code': 205, 'history': h_dict}))
            if request.websocket:
                for message in request.websocket:
                    if not message:
                        break
                    else:
                        message = json.loads(message.decode('utf-8'), strict=False)
                        # print(message)
                        if message['code'] == 204:
                            del_u = UserListModel.objects.filter(customer_id=message['user_id']).first()
                            del_dict = eval(del_u.y_list)
                            del del_dict[message['del_user_id']]
                            del_u.y_list = str(del_dict)
                            del_u.save()
                            print('chengg')
                        elif message['code'] == 203:
                            bond = [message['user_id'], message['to_user_id']]
                            bond.sort()
                            history = HistoryRecord.objects.filter(bond=str(bond)).first()
                            his_list = eval(history.record)
                            his_list[-1]['is_read'] = True
                            # print(his_list)
                            history.record = str(his_list)
                            history.save()
                            # pass
                        elif message['code'] == 202:


                            customer = UserListModel.objects.filter(customer_id=message['to_user_id']).first()
                            if customer:
                                customer_dic = eval(customer.y_list)
                                if user_id not in customer_dic:
                                    customer_dic[user_id] = {'username': user.username, 'img': user.img, 'id': user.id,
                                                             'datetime': str(datetime.datetime.now())}
                                    customer.y_list = str(customer_dic)
                                    customer.save()
                                    if message['to_user_id'] in cli_list:
                                        clients[message['to_user_id']].send(
                                            json.dumps({'code': 200, 'y_list': eval(customer.y_list)}))
                            else:
                                user_c = UserListModel.objects.create(customer_id=message['to_user_id'], y_list=str(
                                    {user_id: {'username': user.username, 'img': user.img, 'id': user.id,
                                               'datetime': str(datetime.datetime.now())}}))
                                if message['to_user_id'] in cli_list:
                                    clients[message['to_user_id']].send(
                                        json.dumps({'code': 200, 'y_list': eval(user_c.y_list)}))

                            # TODO:存记录
                            if 'img_url' in message.keys():
                                # print(message['file_HZ'])
                                obj = {'code': 202, 'msg': message['text'], 'user_id': message['user_id'],
                                       'img': user.img, 'img_url': message['img_url'],
                                       'to_user_id': message['to_user_id'], 'time_str': str(datetime.datetime.now()),
                                       'is_read': False}
                            else:
                                obj = {'code': 202, 'msg': message['text'], 'user_id': message['user_id'], 'img': user.img,
                                   'to_user_id': message['to_user_id'], 'time_str': str(datetime.datetime.now()), 'is_read': False}
                            print(obj)
                            if obj['code'] == 202:
                                bond = [user_id, message['to_user_id']]
                                bond.sort()
                                history = HistoryRecord.objects.filter(bond=str(bond)).first()
                                if history:
                                    print('gengxin')
                                    x = eval(history.record)
                                    if len(x) > 50:
                                        if 'img_url' in x[0]:
                                            os.remove('/var/www/html/static/images/landimages/' + x[0]['img_url'])
                                            print('删除图片成功')
                                        del x[0]

                                    x.append(obj)
                                    history.record = str(x)
                                    history.save()
                                else:
                                    HistoryRecord.objects.create(bond=str(bond), record=str([obj]))
                                    print('新建')
                                if message['to_user_id'] in cli_list:
                                    clients[message['to_user_id']].send(json.dumps(obj))

                                else:
                                    # TODO:告知对方不在线
                                    n_obj = {'code': 303, 'time_str': str(datetime.datetime.now())}
                                    clients[user_id].send(json.dumps(n_obj))
                        # elif obj['code'] == 204:
                        #     UserListModel.objects.filter()
                        #     clients.get(message['to_user_id']).close()
                        #     cli_list.remove(message['to_user_id'])
                        #     del clients[message['to_user_id']]
                        #     pass

        except:
            pass

        # finally:
            # 通过用户名找到 连接信息 再通过 连接信息 k 找到 v (k就是连接信息)
            # clients.get(user_id).close()
            # cli_list.remove(user_id)
            # del clients[user_id]
            # 释放锁
            # lock.release()

