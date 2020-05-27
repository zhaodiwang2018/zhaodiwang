from rest_framework.views import APIView, Response
from .foms import *
from apps.user.serializers import *
from apps.utils.parsing import Parsing
from apps.utils.mixin_utils import *


# TODO：注册后编辑个人资料
class SelfEditView(LoginRequiredMixin, APIView):

    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request))
        if user[0].usertype == '1':
            seria = SelfEditSerializer(user, many=True)
            return Response({'data': seria.data, 'status': '1', 'msg': '获取成功'})
        else:
            seria = EditSerializer(user, many=True)
            return Response({'data': seria.data, 'status': '1', 'msg': '获取成功'})

    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        img = request.data.get('img')
        suffix = request.data.get('suffix')
        form = SelfEditForm(request.data)
        if suffix:
            img = Parsing(img, suffix)
            user.img = img
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:

                user.job = data['job']
                user.username = data['username']
                user.company = data['company']
                user.addr = data['addr']
                user.address_scale = data['address_scale']
                user.plot_ratio = data['plot_ratio']
                user.invest_pattern = data['invest_pattern']
                user.land_nature = data['land_nature']
                user.city = data['city']
                user.area = data['area']
                user.save()
                if user.usertype == '1':
                    self_paiming = PaiMing.objects.filter(user_id=user.id).first()
                    self_paiming.username = user.username
                    self_paiming.save()
                    print('排名添加成功')
            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功', 'data': user.img})
        return Response({'status': '0', 'msg': '数据不完整'})

    def put(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        img = request.data.get('img')
        suffix = request.data.get('suffix')
        form = EditForm(request.data)
        if suffix:

            img = Parsing(img, suffix)
            user.img = img
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user.job = data['job']
                user.username = data['username']
                user.company = data['company']
                user.addr = data['addr']
                user.city = data['city']
                user.area = data['area']
                user.intro = data['intro']
                user.save()

            except:
                return Response({'status': '0', 'msg': '创建失败'})
            return Response({'status': '1', 'msg': '编辑成功', 'data': user.img})
        return Response({'status': '0', 'msg': '数据不完整'})
