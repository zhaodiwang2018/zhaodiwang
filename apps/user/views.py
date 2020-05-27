from rest_framework.views import APIView, Response
from apps.user.models import *
from apps.index.models import *
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from django.contrib.auth.hashers import make_password, check_password
from apps.user.constants import SMS_CODE_REDIS_EXPIRES, SEND_SMS_CODE_INTERVAL
from django_redis import get_redis_connection
from apps.utils.mixin_utils import *
from apps.user.smsnotice import *
import re
import datetime
import pytz
import time
import random
# Create your views here.


class VerifyMobileView(APIView):

    def get(self, request):
        # print(request.META.get("HTTP_AUTHORIZATION"))
        mobile = request.GET.get('mobile')
        ret = re.match(r"^1[35678]\d{9}$", str(mobile))
        if not ret:
            return Response({"msg": "无效手机号", "status": '0'})
        try:
            count = Users.objects.filter(mobile=mobile).count()
        except:
            count = 0
        if count != 0:
            return Response({"msg": "手机号已存在!", "status": '0'})
        else:
            return Response({"msg": "手机号未被注册", "status": '1'})


class Ucpass(object):
    def __init__(self, mobile, sms_code):
        self.mobile = mobile
        self.sms_code = sms_code
        self.apikey = "31df217fdc515fdd2d53f48171917245"

    def send_sms(self):
        # 初始化client,apikey作为所有请求的默认值
        clnt = YunpianClient(self.apikey)
        # 自己定义的短信内容，但要和后台模板相匹配才行
        # param = {YC.MOBILE: self.mobile, YC.TEXT: self.text}
        # r = clnt.sms().single_send(param)
        param = {YC.MOBILE: self.mobile, YC.TPL_ID: '2789228', YC.TPL_VALUE: '#code#=%s' % self.sms_code}
        r = clnt.sms().tpl_single_send(param)
        # print(r.code(), r.data(), r.msg())
        return r.msg()
        # 获取返回结果, 返回码:r.code(),返回码描述:r.msg(),API结果:r.data(),其他说明:r.detail(),调用异常:r.exception()
        # 短信:clnt.sms() 账户:clnt.user() 签名:clnt.sign() 模版:clnt.tpl() 语音:clnt.voice() 流量:clnt.flow()


class SmsCodeView(APIView):
    """发送短信验证码"""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get(self, request):
        mobile = request.GET.get('mobile')
        if mobile is not None:
            sms_code = "%06d" % random.randint(0, 999999)
            # print("验证码：%s" % sms_code)
            redis_conn = get_redis_connection('verify_codes')

            pl = redis_conn.pipeline()
            pl.setex("sms_%s" % mobile, SMS_CODE_REDIS_EXPIRES, sms_code)
            pl.setex('send_flag_%s' % mobile, SEND_SMS_CODE_INTERVAL, 1)
            pl.execute()

            send_flag = redis_conn.get('send_flag_%s' % mobile)
            if int(send_flag) > 1:
                return Response({"msg": "操作太过频繁！", "status": '0'})
            # 发送短信验证码
            # send_sms_code.delay(mobile, sms_code)
            try:
                ccp = Ucpass(mobile, sms_code)
                # ccp.send_sms()
                return Response({"msg": ccp.send_sms(), "status": '1'})
            except Exception as e:
                return Response({"msg": "发送失败!", "status": '0'})
        return Response({"msg": "手机号为空!", "status": '0'})


class RegisterView(APIView):

    def post(self, request):

        """
        注册
        :param request: mobile, password,verify,user_type
        :return: msg
        """
        mobile = request.data.get("mobile")
        yaoqing_zhuce_id = request.data.get('yaoqing_zhuce_id')
        user = Users.objects.filter(mobile=mobile).first()
        is_mode = request.data.get('is_mode')
        if not user:
            password = request.data.get("password")
            # 同时含有数字和字母，且长度要在8-16位之间
            ret = re.match(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$', password)
            if not ret:
                return Response({'msg': '密码不符合规定', 'status': '0'})
            makepwd = make_password(password)
            # print(mobile, password)
            # print("加密的密码： %s" % makepwd)
            verify = request.data.get("verify")

            user_type = request.data.get("usertype")
            redis_conn = get_redis_connection('verify_codes')
            redis_sms_code = redis_conn.get('sms_%s' % mobile)
            if not redis_sms_code:
                return Response({"msg": "验证码已过期!", "status": '0'})
            if redis_sms_code.decode() != verify:
                return Response({"msg": "验证码输入有误!", "status": '0'})
            data = {}
            try:
                user_token = UserToken()
                token = user_token.create_token(mobile + is_mode)
                user = Users.objects.create(mobile=mobile, password=makepwd, usertype=user_type, username=mobile, token=token, integration=99)
                data['username'] = user.username
                data['usertype'] = user.usertype
                data['mobile'] = user.mobile
                data['user_id'] = user.id
                data['token'] = user.token
                data['img'] = user.img
                # SingleVip()
                # TODO: 如果是通过被邀请注册的，则执行
                if yaoqing_zhuce_id:
                    # if int(yaoqing_zhuce_id) != user.id:
                    user.integration += 100
                    user.y_int += 100
                    user.save()
                    yaoqing_content = '恭喜您被邀请注册，并获得100积分'
                    SystemMessageModel.objects.create(content=yaoqing_content, sys_type='被邀请注册所获积分', user_id=user.id)
                    IntegralRecord.objects.create(integral_type='被邀请注册积分', integral=100, user_id=user.id)

                    yaoqing_user = Users.objects.filter(id=int(yaoqing_zhuce_id)).first()
                    yaoqing_user.integration += 100
                    yaoqing_user.y_int += 100
                    yaoqing_user.save()
                    content = '恭喜您成功邀请{}注册找地网，您已获得100积分，可到个人中心查看。'.format(user.username)
                    SystemMessageModel.objects.create(content=content, sys_type='邀请注册获得积分', user_id=yaoqing_user.id)
                    IntegralRecord.objects.create(integral_type='邀请注册获得积分', integral=100, user_id=yaoqing_user.id)
                    InviteRegister.objects.create(invite_peo_id=int(yaoqing_zhuce_id), register_peo_id=user.id, yq_type='邀请注册')
                    NeiCe.objects.create(user_id=user.id, leibie='注册')
                    if yaoqing_user.usertype == '1':
                        paiming = PaiMing.objects.filter(user_id=yaoqing_user.id).first()
                        paiming.act_num += 30
                        paiming.save()
                today = datetime.date.today()
                today_data = AdminUserChart.objects.filter(create_on=today).first()
                if today_data:
                    today_data.new_user += 1
                    today_data.user_all += 1
                    today_data.save()
                else:
                    user_num = Users.objects.count()
                    AdminUserChart.objects.create(new_user=1, user_all=user_num)
                if user.usertype == '1':
                    PaiMing.objects.create(username=user.username, act_num=user.integration * 0.3, user_id=user.id)
                return Response({"data": data, 'status': '1', 'message': '注册成功'})
            except:
                return Response({'status': '0', 'msg': '注册失败'})
        return Response({'status': '0', 'msg': '无效'})


class ForgetPasswordView(APIView):

    def post(self, request):
        """
        忘记密码
        :param request: mobile, verify
        :return: msg
        """
        mobile = request.data.get("mobile", '18608643826')
        user = Users.objects.filter(mobile=mobile).first()
        if not user:
            return Response({'msg': '该用户不存在', 'status': '0'})
        verify = request.data.get("verify", '976157')
        redis_conn = get_redis_connection('verify_codes')
        redis_sms_code = redis_conn.get('sms_%s' % mobile)
        if not redis_sms_code:
            return Response({"msg": "验证码已过期!", "status": '0'})
        if redis_sms_code.decode() != verify:
            return Response({"msg": "验证码输入有误!", "status": '0'})
        return Response({"msg": "验证成功!", "status": '1'})

    def put(self, request):
        mobile = request.data.get("mobile", '18608643826')
        user = Users.objects.filter(mobile=mobile).first()
        if user:
            password = request.data.get('password')
            ret = re.match(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$', password)
            if not ret:
                return Response({'msg': '密码不符合规定', 'status': '0'})
            makepwd = make_password(password)
            try:
                user.password = makepwd
                user.save()
                return Response({'msg': '修改成功', 'status': '1'})
            except:
                return Response({'msg': '修改失败', 'status': '0'})
        return Response({'msg': '该用户不存在', 'status': '0'})


class LoginView(APIView):

    def post(self, request):
        print(request)
        mobile = request.data.get("mobile")
        print(mobile)
        password = request.data.get('password')
        is_mode = request.data.get('is_mode')
        print(is_mode)
        user = Users.objects.filter(mobile=mobile).first()
        if not user:
            return Response({'msg': '该用户不存在', 'status': '0'})
        if user.status == 0:
            return Response({'msg': '账户冻结', 'status': '0'})
        data = {}
        if user and check_password(password, user.password):
            user_token = UserToken()
            token = user_token.create_token(mobile + is_mode)
            user.token = token
            user.login_num += 1
            user.save()
            data['username'] = user.username
            data['usertype'] = user.usertype
            data['mobile'] = user.mobile
            data['user_id'] = user.id
            data['token'] = user.token
            data['img'] = user.img
            data['vip_num'] = user.vip_num
            # TODO：登录判断会员是否到期
            a = VipExpire.objects.filter(user_id=user.id).first()
            if a:
                if datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')) < a.expire_time.replace(tzinfo=pytz.timezone('UTC')):
                    data['expire'] = True
                else:
                    data['vip_num'] = 0
                    user.vip_num = 0
                    user.save()
                    a.delete()
                    data['expire'] = False
            today = datetime.date.today()
            today_str = time.mktime(today.timetuple())
            login_a = LoginRecord.objects.filter(user_id=user.id).last()
            if login_a:
                t = datetime.datetime(login_a.create_on.year, login_a.create_on.month, login_a.create_on.day, 0, 0, 0)
                time_array = time.mktime(t.timetuple())
                if time_array != today_str:
                    LoginRecord.objects.create(user_id=user.id)
            else:
                LoginRecord.objects.create(user_id=user.id)

            # TODO:信息不完善时，以此字段判定，跳转编辑个人信息页面
            if not user.company:
                data['imperfect'] = False
            return Response({"data": data, 'msg': '登录成功', 'status': '1'})
        return Response({'msg': '用户名或密码错误', 'status': '0'})


# 管理员登录
class AdminLoginView(APIView):
    # TODO:未拼接token
    def post(self, request):
        mobile = request.data.get("mobile")
        password = request.data.get('password')
        user = Users.objects.filter(mobile=mobile).first()
        if not user:
            return Response({'msg': '该用户不存在', 'status': '0'})
        if user.status == 0:
            return Response({'msg': '账户冻结', 'status': '0'})
        if user.is_admin == 0:
            return Response({'msg': '非管理账户，无权登录', 'status': '0'})
        data = {}
        if mobile == '12345678910':
            data['isALLadmin'] = False
        else:
            data['isALLadmin'] = True
        if user and check_password(password, user.password):
            user_token = UserToken()
            token = user_token.create_token(mobile)
            user.token = token
            user.login_num += 1
            user.save()
            data['username'] = user.username
            data['usertype'] = user.usertype
            data['mobile'] = user.mobile
            data['user_id'] = user.id

            data['token'] = user.token
            data['img'] = user.img
            return Response({"data": data, 'msg': '登录成功', 'status': '1'})
        return Response({'msg': '用户名或密码错误', 'status': '0'})

    def put(self,request):
        user_id = request.data.get('user_id')
        user = Users.objects.filter(id=user_id).first()
        user.status = 0
        user.save()
        return Response({'msg': '账户冻结成功', 'status': '1'})


class UpdateDataView(APIView):
    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        data = {'username': user.username, 'mobile': user.mobile, 'vip_num': user.vip_num, 'usertype': user.usertype}
        return Response({'msg': '成功', 'status': '1', 'data': data})









