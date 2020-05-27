from rest_framework import serializers
from apps.user.models import *


class SelfEditSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = ('job', 'company', 'addr', 'address_scale', 'username', 'img',
                  'plot_ratio', 'invest_pattern', 'land_nature', 'city', 'area')

    def get_img(self, obj):
        return 'http://118.31.60.22/static/images/landimages/' + obj.img


class EditSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ('job', 'company', 'addr', 'username', 'img', 'city', 'area', 'intro')

    def get_img(self, obj):
        return 'http://118.31.60.22/static/images/landimages/' + obj.img


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('pay_time', 'order_mount', 'subject', 'pay_status', 'order_sn')











