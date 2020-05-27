# -*- coding: UTF-8 -*-
# __author__ : qindi
# __data__  : 2019/7/16


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from apps.utils.token_utils import UserToken


# 获取浏览器header
def get_header_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    # print('con', token)
    return token


# TODO：通过token获取user_id
def get_user_id(request):
    token = UserToken()
    return token.get_username(get_header_token(request))[:11]


def my_login_required(func):
    """自定义 登录验证 装饰器"""

    def check_login_status(request):
        """检查登录状态"""
        ut = UserToken()
        token = get_header_token(request)
        res = ut.check_token(token)
        # print(res)
        if res:
            # 当前有用户登录，正常跳转
            return func(request)
        else:
            # 当前没有用户登录，跳转到登录页面
            data = {'msg': '过期'}
            print(data)
            return HttpResponse(data)

    return check_login_status


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **init_kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**init_kwargs)
        return my_login_required(view)
