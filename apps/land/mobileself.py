# -*- coding: utf-8 -*-
# @Time    : 2019/9/20 16:25
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : mobileself.py
# @Software: PyCharm


from rest_framework.views import APIView, Response
from apps.land.forms import *
from apps.user.models import *
from apps.utils.mixin_utils import *


class MobileSelf(APIView):
    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        user_id = user.id
        data = {}
        nitui_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/nitui', user_id=user_id, ).count()
        paimai_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/paimai', user_id=user_id, ).count()
        guapai_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/guapai', user_id=user_id, ).count()
        zhuanrang_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/zhuanrang', user_id=user_id, ).count()
        zhaoshang_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/zhaoshang', user_id=user_id, ).count()
        xiancheng_receive_num = ReceivePeo.objects.filter(luyou='/tudimessage/xiancheng', user_id=user_id, ).count()
        project_receives = nitui_receive_num + paimai_receive_num + guapai_receive_num + zhuanrang_receive_num + zhaoshang_receive_num + xiancheng_receive_num
        # 联系
        nitui_contact_num = Contact.objects.filter(luyou='/tudimessage/nitui', user_id=user_id, ).count()
        paimai_contact_num = Contact.objects.filter(luyou='/tudimessage/paimai', user_id=user_id, ).count()
        guapai_contact_num = Contact.objects.filter(luyou='/tudimessage/guapai', user_id=user_id, ).count()
        zhuanrang_contact_num = Contact.objects.filter(luyou='/tudimessage/zhuanrang', user_id=user_id, ).count()
        zhaoshang_contact_num = Contact.objects.filter(luyou='/tudimessage/zhaoshang', user_id=user_id, ).count()
        xiancheng_contact_num = Contact.objects.filter(luyou='/tudimessage/xiancheng', user_id=user_id, ).count()
        # 被联系
        paimai_contacted_num = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/paimai').count()
        zhuanrang_contacted_num = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/zhuanrang').count()
        zhaoshang_contacted_num = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/zhaoshang').count()
        xiancheng_contacted_num = Contact.objects.filter(contacted_id=user_id, luyou='/tudimessage/xiancheng').count()

        data['111'] = project_receives

        data[
            '114'] = nitui_contact_num + paimai_contact_num + guapai_contact_num + zhuanrang_contact_num + zhaoshang_contact_num + xiancheng_contact_num
        data[
            '115'] = paimai_contacted_num + zhuanrang_contacted_num + zhaoshang_contacted_num + xiancheng_contacted_num

        return Response({'msg': '获取成功', 'status': '1', 'kandi_data': data['111'], 'lianxi': data['114'] + data['115'], 'jifen': user.integration})
