from django.shortcuts import render
from rest_framework.views import APIView, Response
from apps.utils.mixin_utils import LoginRequiredMixin
from apps.utils.parsing import Parsing


class UpImag(APIView):
    def post(self, request):
        img = request.data.get('img')
        suffix = request.data.get('suffix')
        if not img:
            return Response({'msg': 'img没传', 'status': '0'})
        data = {'img_name': Parsing(img, suffix)}
        return Response({'data': data, 'msg': '上传成功', 'status': '1'})
