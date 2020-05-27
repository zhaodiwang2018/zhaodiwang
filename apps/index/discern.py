# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 17:25
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : discern.py
# @Software: PyCharm
from rest_framework.views import APIView, Response
from apps.index.models import *
from apps.user.models import *
from rest_framework import serializers
from apps.utils.mixin_utils import *
import datetime, pytz


class IntegralRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = IntegralRecord
        fields = ('create_on', 'integral_type', 'integral')


# 积分记录
class IntegralRecordView(LoginRequiredMixin, APIView):

    def get(self, request):
        page = int(request.GET.get('page', 1))
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        record = IntegralRecord.objects.filter(user_id=user.id, ).order_by('-id')[(page - 1) * 4:(page - 1) * 4 + 4]
        count = IntegralRecord.objects.filter(user_id=user.id).count()
        seria = IntegralRecordSerializers(record, many=True)
        return Response({'msg': '成功', 'status': '1', 'data': seria.data, 'count': count, 'jifen': user.integration})


class YaoQingZhuCeSerializers(serializers.ModelSerializer):
    beiyaoqingren = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = InviteRegister
        fields = ('create_on', 'beiyaoqingren', 'img')

    def get_beiyaoqingren(self, obj):
        if obj:
            beiyaoqing_user = Users.objects.filter(id=obj.register_peo_id).first()
            return beiyaoqing_user.username
        return ''

    def get_img(self, obj):
        if obj:
            beiyaoqing_user = Users.objects.filter(id=obj.register_peo_id).first()
            return beiyaoqing_user.img
        return ''


# 邀请记录
class YaoQingZhuCeView(LoginRequiredMixin, APIView):
    # 邀请注册记录
    def get(self, request):
        user_id = request.GET.get('user_id')
        if user_id:
            user = Users.objects.filter(id=int(user_id)).first()
        else:
            user = Users.objects.filter(mobile=get_user_id(request)).first()
        record = InviteRegister.objects.filter(invite_peo_id=user.id, yq_type='邀请注册').order_by('-id')
        seria = YaoQingZhuCeSerializers(record, many=True)
        return Response({'msg': '成功', 'status': '1', 'data': seria.data})

    # 邀请付费记录
    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        record = InviteRegister.objects.filter(invite_peo_id=user.id, yq_type='邀请付费').order_by('-id')
        seria = YaoQingZhuCeSerializers(record, many=True)
        return Response({'msg': '成功', 'status': '1', 'data': seria.data})


class YaoQingHomePage(LoginRequiredMixin, APIView):
    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        y_num = InviteRegister.objects.filter(invite_peo_id=user.id).count()
        return Response({'msg': '成功', 'status': '1', 'yq_num': y_num, 'jf': user.y_int})


class GetUserNameView(APIView):

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = Users.objects.filter(id=int(user_id)).first()
        return Response({'msg': '成功', 'status': '1', 'username': user.username})



class DiscernSerializers(serializers.ModelSerializer):
    class Meta:
        model = Discern
        fields = ('first_question', 'second_question', 'third_question', 'fourth_question', 'fifth_question')


# 挑刺报名 TODO：get（获取挑刺报名的五个问题） post（提交五个问题， 包含被邀请挑刺）
class DiscernView(APIView):

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        question_info = Discern.objects.filter(user_id=user.id)
        seria = DiscernSerializers(question_info, many=True)
        return Response({'msg': '成功', 'status': '1', 'data': seria.data})

    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        yaoqing_tiaoci_id = request.data.get('yaoqing_tiaoci_id')
        first_question = request.data.get('first_question')
        second_question = request.data.get('second_question')
        third_question = request.data.get('third_question')
        fourth_question = request.data.get('fourth_question')
        fifth_question = request.data.get('fifth_question')
        Discern.objects.create(first_question=first_question, second_question=second_question,
                               third_question=third_question, fourth_question=fourth_question,
                               fifth_question=fifth_question, user_id=user.id)
        user.integration += 129
        user.t_int += 129
        user.save()
        content = '恭喜您成功参加挑刺活动，您已获得60积分，可到个人中心查看。经找地网相关部门审核后，将会根据其价值奖励更多积分。'
        SystemMessageModel.objects.create(content=content, sys_type='基础积分', user_id=user.id)
        IntegralRecord.objects.create(integral_type='报名基础积分', integral=129, user_id=user.id)
        # TODO:如果是被邀请挑刺的，则执行
        if yaoqing_tiaoci_id:
            if int(yaoqing_tiaoci_id) != user.id:
                user.integration += 100
                user.t_int += 100
                user.save()
                yaoqing_content = '恭喜您被邀请参见挑刺活动，并获得100积分'
                SystemMessageModel.objects.create(content=yaoqing_content, sys_type='被邀请挑刺所获积分', user_id=user.id)
                IntegralRecord.objects.create(integral_type='被邀请挑刺积分', integral=100, user_id=user.id)

                yaoqing_user = Users.objects.filter(id=int(yaoqing_tiaoci_id)).first()
                yaoqing_user.integration += 100
                yaoqing_user.t_int += 100
                yaoqing_user.save()
                content = '恭喜您成功邀请{}参加挑刺活动，您已获得99积分，可到个人中心查看。'.format(user.username)
                SystemMessageModel.objects.create(content=content, sys_type='邀请挑刺获得积分', user_id=yaoqing_user.id)
                IntegralRecord.objects.create(integral_type='邀请挑刺获得积分', integral=99, user_id=yaoqing_user.id)
        return Response({'msg': '成功', 'status': '1'})


class DiscernAuditSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Discern
        fields = (
        'user_id', 'first_question', 'second_question', 'third_question', 'fourth_question', 'fifth_question', 'fen',
        'username', 'state')

    def get_username(self, obj):
        if obj:
            user = Users.objects.filter(id=obj.user_id).first()
            return user.username
        return ''


# 审核刺
class DiscernAuditView(APIView):
    def get(self, request):
        page = int(request.GET.get('page'))
        cis = Discern.objects.all().order_by('-id')[(page - 1) * 10:(page - 1) * 10 + 10]
        total_page = Discern.objects.all().count()
        seria = DiscernAuditSerializers(cis, many=True)
        return Response({'msg': '成功', 'status': '1', 'data': seria.data, 'total_page': total_page})

    def post(self, request):
        user_id = request.data.get('user_id')
        discern = Discern.objects.filter(user_id=user_id).first()
        if discern.state == 1:
            return Response({'msg': '已审核', 'status': '0'})
        integration = request.data.get('integration')
        user = Users.objects.filter(id=user_id).first()
        user.integration += integration
        user.t_int += integration
        user.save()
        discern.state = 1
        discern.fen += integration
        discern.save()
        content = '感谢参加挑刺活动，经审核，您获得{}积分，可到个人中心查看。稍后将会公布前20名！尽情期待！'.format(integration)
        SystemMessageModel.objects.create(content=content, sys_type='审核挑刺获得积分', user_id=user_id)
        IntegralRecord.objects.create(integral_type='审核挑刺获得积分', integral=integration, user_id=user_id)
        return Response({'msg': '成功', 'status': '1'})


# 判断是否已填写问题
class IsOkView(APIView):

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'msg': '请登录', 'status': '0'})
        user = Users.objects.filter(id=int(user_id)).first()
        neice = NeiCe.objects.filter(user_id=user.id, leibie='内测').first()
        if neice:
            return Response({'msg': '内测报名成功', 'status': '3', 'data': user.t_int})
        # TODO：报名截止后停掉1，2
        info = Discern.objects.filter(user_id=user.id).first()
        if not info:
            return Response({'msg': '未填写', 'status': '1'})
        return Response({'msg': '已填写', 'status': '2', 'data': user.t_int})


class IsSuccessView(APIView):

    def get(self, request):
        # user_id = request.GET.get('user_id')
        # if not user_id:
        #     re
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        data = []
        neice = NeiCe.objects.filter(user_id=user.id, leibie='内测').first()
        zhuce = NeiCe.objects.filter(user_id=user.id, leibie='注册').first()
        yaoqing = NeiCe.objects.filter(user_id=user.id, leibie='邀请').first()
        if neice:
            if neice.user_status == 0:
                neice.user_status = 1
                neice.save()
                nc = {'neice': True}
            else:
                nc = {'neice': False}
            data.append(nc)
        if zhuce:
            if zhuce.user_status == 0:
                zhuce.user_status = 1
                zhuce.save()
                zc = {'zhuce': True}
            else:
                zc = {'zhuce': False}
            data.append(zc)
        if yaoqing:
            if yaoqing.user_status == 0:
                yaoqing.user_status = 1
                yaoqing.save()
                yq = {'yaoqing': True}
            else:
                yq = {'yaoqing': False}
            data.append(yq)
        return Response({'msg': '成功', 'status': '1', 'data': data})


# 积分抵会员
class JiFenVipView(APIView):
    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        vip_type = request.data.get('vip_type')
        if vip_type == '年':
            vip_integral = 50000
            if user.integration < vip_integral:
                return Response({'msg': '积分不足', 'status': '0'})
            user.integration -= vip_integral
            vip_num = 4
            days = 365
        elif vip_type == '季':
            vip_integral = 13800
            if user.integration < vip_integral:
                return Response({'msg': '积分不足', 'status': '0'})
            user.integration -= vip_integral
            vip_num = 3
            days = 90

        elif vip_type == '月':
            vip_integral = 5000
            if user.integration < vip_integral:
                return Response({'msg': '积分不足', 'status': '0'})
            user.integration -= vip_integral
            vip_num = 2
            days = 30
        else:
            return Response({'msg': '数据错误', 'status': '0'})
        user.save()
        vip = VipExpire.objects.filter(user_id=user.id).first()
        if vip:
            # 如果没到期
            if vip.expire_time.replace(tzinfo=pytz.timezone('UTC')) > datetime.datetime.now().replace(
                    tzinfo=pytz.timezone('UTC')):
                vip.expire_time = vip.expire_time.replace(tzinfo=pytz.timezone('UTC')) + datetime.timedelta(days=days)
                vip.save()
            else:
                vip.expire_time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')) + datetime.timedelta(
                    days=days)
                vip.save()
            if user.vip_num <= vip_num:
                user.vip_num = vip_num
                user.save()
            else:
                user.vip_num = user.vip_num
                user.save()
        else:
            VipExpire.objects.create(user_id=user.id, expire_time=datetime.datetime.now().replace(
                tzinfo=pytz.timezone('UTC')) + datetime.timedelta(days=days))
            user.vip_num = vip_num
            user.save()
        content = '恭喜您成功使用积分，成为' + vip_type + '会员'
        SystemMessageModel.objects.create(content=content, sys_type='会员充值', user_id=user.id, )
        IntegralRecord.objects.create(integral_type='积分抵扣会员', integral=vip_integral, user_id=user.id)
        return Response({'msg': '成功', 'status': '1'})
