from rest_framework import serializers
from apps.land.models import *
from apps.user.models import *


class LandSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = LandInfo
        fields = ('id', 'title', 'luyou', 'img', 'desc', 'create_on', 'audit_state')

    def get_luyou(self, obj):
        if obj.land_type == '1':
            return '/tudimessage/guapai'
        elif obj.land_type == '2':
            return '/tudimessage/nitui'
        elif obj.land_type == '3':
            return '/tudimessage/paimai'
        elif obj.land_type == '4':
            return '/tudimessage/xiancheng'
        else:
            return '错误'


class TransSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = TransInfo
        fields = ('id', 'title', 'img', 'luyou', 'desc', 'create_on', 'audit_state')

    def get_luyou(self, obj):
        return '/tudimessage/zhuanrang'


class AttractSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = AttractInfo
        fields = ('id', 'title', 'luyou', 'img', 'desc', 'create_on', 'audit_state')

    def get_luyou(self, obj):
        return '/tudimessage/zhaoshang'


class ActivityListSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('id', 'title', 'img', 'luyou', 'desc', 'create_on', 'audit_state')

    def get_luyou(self, obj):
        if obj.activity_type == '1':
            return '/activity/shalong'
        elif obj.activity_type == '2':
            return '/activity/yuebao'
        elif obj.activity_type == '3':
            return '/activity/tuijie'
        elif obj.activity_type == '4':
            return '/activity/kuanian'


class PropertyListSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = PropertyList
        fields = ('id', 'title', 'img', 'luyou', 'desc', 'create_on', 'audit_state')

    def get_luyou(self, obj):
        if obj.property_type == '1':
            return "/tudilist/nadi"
        elif obj.property_type == '2':
            return "/tudilist/gongdi"
        elif obj.property_type == '3':
            return "/tudilist/shoulou"
        elif obj.property_type == '4':
            return "/tudilist/loupan"


class InvestmentDataSerializers(serializers.ModelSerializer):
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = InvestmentData
        fields = ('id', 'title', 'img', 'luyou', 'desc', 'create_on', 'audit_state')

    def get_luyou(self, obj):
        if obj.property_type == '1':
            return "/Investment/zhoubao"
        elif obj.property_type == '2':
            return "/Investment/yuebao"
        elif obj.property_type == '3':
            return "/Investment/jibao"
        elif obj.property_type == '4':
            return "/Investment/bannianbao"
        elif obj.property_type == '5':
            return "/Investment/nianbao"


class LandDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = LandInfo
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'create_on', 'information_source', 'reward_price', 'land_type'
        )


class TransDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = TransInfo
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'create_on', 'information_source', 'reward_price')


class AttractDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = AttractInfo
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'create_on', 'information_source', 'reward_price')


class ActivityDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'activity_datetime', 'activity_place', 'information_source',
            'reward_price', 'create_on', 'activity_type', 'traffic_tips', 'quota', 'content_feed')


class PropertyListDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = PropertyList
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'reward_price', 'information_source', 'create_on',
            'information_source', 'file_introduction', 'property_type', 'file_url')


class InvestmentDataDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = InvestmentData
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'reward_price', 'information_source', 'create_on',
            'information_source', 'file_introduction', 'property_type', 'file_url')


class NoticeListSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    land_type = serializers.SerializerMethodField()
    jieshou = serializers.SerializerMethodField()
    chakan = serializers.SerializerMethodField()
    shoucang = serializers.SerializerMethodField()
    lianxi = serializers.SerializerMethodField()
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = LandInfo
        fields = ('id', 'city', 'title', 'username', 'create_on', 'area', 'location', 'serial_number', 'land_type',
                  'land_area', 'plot_ratio', 'audit_state', 'land_type', 'jieshou', 'chakan', 'shoucang', 'lianxi', 'luyou')

    def get_username(self, obj):
        release = ReleaseRecord.objects.filter(land_id=obj.id, luyou__in=['/tudimessage/nitui', '/tudimessage/paimai',
                                                                          '/tudimessage/guapai',
                                                                          '/tudimessage/xiancheng']).first()
        user = Users.objects.filter(id=release.user_id).first()
        return user.username

    def get_land_type(self, obj):
        if obj.land_type == '1':
            return '挂牌公告'
        elif obj.land_type == '2':
            return '拟推预告'
        elif obj.land_type == '3':
            return '拍卖公告'
        elif obj.land_type == '4':
            return '县城土地'

    def get_luyou(self, obj):
        if obj.land_type == '1':
            return '/tudimessage/guapai'
        elif obj.land_type == '2':
            return '/tudimessage/nitui'
        elif obj.land_type == '3':
            return '/tudimessage/paimai'
        elif obj.land_type == '4':
            return '/tudimessage/xiancheng'

    def get_jieshou(self, obj):
        return Users.objects.filter(city__contains=obj.city).count()

    def get_chakan(self, obj):
        if obj.land_type == '1':
            count = ReceivePeo.objects.filter(luyou='/tudimessage/guapai', information_id=obj.id).count()
        elif obj.land_type == '2':
            count = ReceivePeo.objects.filter(luyou='/tudimessage/nitui', information_id=obj.id).count()

        elif obj.land_type == '3':
            count = ReceivePeo.objects.filter(luyou='/tudimessage/paimai', information_id=obj.id).count()

        else:
            count = ReceivePeo.objects.filter(luyou='/tudimessage/xiancheng', information_id=obj.id).count()
        return count

    def get_shoucang(self, obj):
        if obj.land_type == '1':
            count = Collection.objects.filter(luyou='/tudimessage/guapai', information_id=obj.id).count()
        elif obj.land_type == '2':
            count = Collection.objects.filter(luyou='/tudimessage/nitui', information_id=obj.id).count()

        elif obj.land_type == '3':
            count = Collection.objects.filter(luyou='/tudimessage/paimai', information_id=obj.id).count()

        else:
            count = Collection.objects.filter(luyou='/tudimessage/xiancheng', information_id=obj.id).count()
        return count

    def get_lianxi(self, obj):
        if obj.land_type == '1':
            count = OrderInfo.objects.filter(luyou='/tudimessage/guapai', land_id=obj.id, pay_status='TRADE_SUCCESS').count()
        elif obj.land_type == '2':
            count = OrderInfo.objects.filter(luyou='/tudimessage/nitui', land_id=obj.id, pay_status='TRADE_SUCCESS').count()

        elif obj.land_type == '3':
            count = OrderInfo.objects.filter(luyou='/tudimessage/paimai', land_id=obj.id, pay_status='TRADE_SUCCESS').count()

        else:
            count = OrderInfo.objects.filter(luyou='/tudimessage/xiancheng', land_id=obj.id, pay_status='TRADE_SUCCESS').count()
        return count


class TransInfoListSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    land_type = serializers.SerializerMethodField()
    jieshou = serializers.SerializerMethodField()
    chakan = serializers.SerializerMethodField()
    shoucang = serializers.SerializerMethodField()
    lianxi = serializers.SerializerMethodField()
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = TransInfo
        fields = ('id', 'create_on', 'title', 'username', 'city', 'location', 'serial_number', 'luyou',
                  'land_area', 'plot_ratio', 'audit_state', 'land_type', 'jieshou', 'chakan', 'shoucang', 'lianxi')

    def get_username(self, obj):
        release = ReleaseRecord.objects.filter(land_id=obj.id, luyou='/tudimessage/zhuanrang').first()
        user = Users.objects.filter(id=release.user_id).first()
        return user.username

    def get_land_type(self, obj):
        if obj:
            return '转让信息'

    def get_luyou(self, obj):
        if obj:
            return '/tudimessage/zhuanrang'

    def get_jieshou(self, obj):
        return Users.objects.filter(city__contains=obj.city).count()

    def get_chakan(self, obj):
        if obj:
            count = ReceivePeo.objects.filter(luyou='/tudimessage/zhuanrang', information_id=obj.id).count()
            return count
        return 0

    def get_shoucang(self, obj):
        if obj:
            count = Collection.objects.filter(luyou='/tudimessage/zhuanrang', information_id=obj.id).count()
            return count
        return 0

    def get_lianxi(self, obj):
        if obj:
            count = OrderInfo.objects.filter(luyou='/tudimessage/zhuanrang', land_id=obj.id, pay_status='TRADE_SUCCESS').count()
            return count
        return 0


class AttractListSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    land_type = serializers.SerializerMethodField()
    jieshou = serializers.SerializerMethodField()
    chakan = serializers.SerializerMethodField()
    shoucang = serializers.SerializerMethodField()
    lianxi = serializers.SerializerMethodField()
    luyou = serializers.SerializerMethodField()

    class Meta:
        model = AttractInfo
        fields = ('id', 'create_on', 'city', 'title', 'username', 'location', 'serial_number', 'land_area', 'total_inv',
                  'audit_state', 'land_type', 'jieshou', 'chakan', 'shoucang', 'lianxi', 'luyou')

    def get_username(self, obj):
        release = ReleaseRecord.objects.filter(land_id=obj.id, luyou='/tudimessage/zhaoshang').first()
        user = Users.objects.filter(id=release.user_id).first()
        return user.username

    def get_land_type(self, obj):
        if obj:
            return '招商信息'

    def get_luyou(self, obj):
        if obj:
            return '/tudimessage/zhaoshang'

    def get_jieshou(self, obj):
        return Users.objects.filter(city__contains=obj.city).count()

    def get_chakan(self, obj):
        if obj:
            count = ReceivePeo.objects.filter(luyou='/tudimessage/zhaoshang', information_id=obj.id).count()
            return count
        return 0

    def get_shoucang(self, obj):
        if obj:
            count = Collection.objects.filter(luyou='/tudimessage/zhaoshang', information_id=obj.id).count()
            return count
        return 0

    def get_lianxi(self, obj):
        if obj:
            count = OrderInfo.objects.filter(luyou='/tudimessage/zhaoshang', land_id=obj.id, pay_status='TRADE_SUCCESS').count()
            return count
        return 0


class ActivitySerializers(serializers.ModelSerializer):
    activity_type = serializers.SerializerMethodField()
    luyou = serializers.SerializerMethodField()
    jishou = serializers.SerializerMethodField()
    chakan = serializers.SerializerMethodField()
    shoucang = serializers.SerializerMethodField()
    baoming = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = (
            'id', 'create_on', 'luyou', 'title', 'activity_type', 'activity_datetime', 'jishou', 'chakan', 'shoucang',
            'baoming', 'audit_state')

    def get_activity_type(self, obj):
        if obj.activity_type == '1':
            return '沙龙'
        elif obj.activity_type == '2':
            return '月报'
        elif obj.activity_type == '3':
            return '推介会'
        elif obj.activity_type == '4':
            return '跨年'

    def get_luyou(self, obj):
        if obj.activity_type == '1':
            return '/activity/shalong'
        elif obj.activity_type == '2':
            return '/activity/yuebao'
        elif obj.activity_type == '3':
            return '/activity/tuijie'
        elif obj.activity_type == '4':
            return '/activity/kuanian'

    def get_jishou(self, obj):
        return Users.objects.all().count()

    def get_chakan(self, obj):
        if obj.activity_type == '1':
            count = ReceivePeo.objects.filter(luyou='/activity/shalong', information_id=obj.id).count()
        elif obj.activity_type == '2':
            count = ReceivePeo.objects.filter(luyou='/activity/yuebao', information_id=obj.id).count()

        elif obj.activity_type == '3':
            count = ReceivePeo.objects.filter(luyou='/activity/tuijie', information_id=obj.id).count()

        else:
            count = ReceivePeo.objects.filter(luyou='/activity/kuanian', information_id=obj.id).count()
        return count

    def get_shoucang(self, obj):
        if obj.activity_type == '1':
            count = Collection.objects.filter(luyou='/activity/shalong', information_id=obj.id).count()
        elif obj.activity_type == '2':
            count = Collection.objects.filter(luyou='/activity/yuebao', information_id=obj.id).count()

        elif obj.activity_type == '3':
            count = Collection.objects.filter(luyou='/activity/tuijie', information_id=obj.id).count()

        else:
            count = Collection.objects.filter(luyou='/activity/kuanian', information_id=obj.id).count()
        return count

    def get_baoming(self, obj):
        if obj.activity_type == '1':
            count = OrderInfo.objects.filter(luyou='/activity/shalong', land_id=obj.id).count()
        elif obj.activity_type == '2':
            count = OrderInfo.objects.filter(luyou='/activity/yuebao', land_id=obj.id).count()

        elif obj.activity_type == '3':
            count = OrderInfo.objects.filter(luyou='/activity/tuijie', land_id=obj.id).count()

        else:
            count = OrderInfo.objects.filter(luyou='/activity/kuanian', land_id=obj.id).count()
        return count


class InvestmentDataListSerializers(serializers.ModelSerializer):
    property_type = serializers.SerializerMethodField()
    jishou = serializers.SerializerMethodField()
    chakan = serializers.SerializerMethodField()
    shoucang = serializers.SerializerMethodField()
    xiazai = serializers.SerializerMethodField()

    class Meta:
        model = PropertyList
        fields = ('id', 'create_on', 'title', 'property_type', 'jishou', 'chakan', 'shoucang', 'xiazai', 'audit_state',)

    def get_property_type(self, obj):
        if obj.property_type == '1':
            return '周报'
        elif obj.property_type == '2':
            return '月报'
        elif obj.property_type == '3':
            return '季报'
        elif obj.property_type == '4':
            return '半年报'
        elif obj.property_type == '5':
            return '年报'

    def get_jishou(self, obj):
        return Users.objects.all().count()

    def get_chakan(self, obj):
        if obj.property_type == '1':
            count = ReceivePeo.objects.filter(luyou='/Investment/zhoubao', information_id=obj.id).count()
        elif obj.property_type == '2':
            count = ReceivePeo.objects.filter(luyou='/Investment/yuebao', information_id=obj.id).count()

        elif obj.property_type == '3':
            count = ReceivePeo.objects.filter(luyou='/Investment/jibao', information_id=obj.id).count()
        elif obj.property_type == '4':
            count = ReceivePeo.objects.filter(luyou='/Investment/bannianbao', information_id=obj.id).count()
        else:
            count = ReceivePeo.objects.filter(luyou='/Investment/nianbao', information_id=obj.id).count()
        return count

    def get_shoucang(self, obj):
        if obj.property_type == '1':
            count = Collection.objects.filter(luyou='/Investment/zhoubao', information_id=obj.id).count()
        elif obj.property_type == '2':
            count = Collection.objects.filter(luyou='/Investment/yuebao', information_id=obj.id).count()

        elif obj.property_type == '3':
            count = Collection.objects.filter(luyou='/Investment/jibao', information_id=obj.id).count()

        elif obj.property_type == '3':
            count = Collection.objects.filter(luyou='/Investment/bannianbao', information_id=obj.id).count()
        else:
            count = Collection.objects.filter(luyou='/Investment/nianbao', information_id=obj.id).count()
        return count

    def get_xiazai(self, obj):
        if obj.property_type == '1':
            count = OrderInfo.objects.filter(luyou='/Investment/zhoubao', land_id=obj.id).count()
        elif obj.property_type == '2':
            count = OrderInfo.objects.filter(luyou='/Investment/yuebao', land_id=obj.id).count()

        elif obj.property_type == '3':
            count = OrderInfo.objects.filter(luyou='/Investment/jibao', land_id=obj.id).count()
        elif obj.property_type == '4':
            count = OrderInfo.objects.filter(luyou='/Investment/bannianbao', land_id=obj.id).count()

        else:
            count = OrderInfo.objects.filter(luyou='/Investment/nianbao', land_id=obj.id).count()
        return count


class PopListSerializers(serializers.ModelSerializer):
    property_type = serializers.SerializerMethodField()
    jishou = serializers.SerializerMethodField()
    chakan = serializers.SerializerMethodField()
    shoucang = serializers.SerializerMethodField()
    xiazai = serializers.SerializerMethodField()

    class Meta:
        model = PropertyList
        fields = (
            'id', 'create_on', 'title', 'property_type', 'jishou', 'chakan', 'shoucang', 'xiazai', 'audit_state',)

    def get_property_type(self, obj):
        if obj.property_type == '1':
            return '企业拿地榜'
        elif obj.property_type == '2':
            return '城市供地榜'
        elif obj.property_type == '3':
            return '城市售楼榜'
        elif obj.property_type == '4':
            return '价值楼盘榜'

    def get_jishou(self, obj):
        return Users.objects.all().count()

    def get_chakan(self, obj):
        if obj.property_type == '1':
            count = ReceivePeo.objects.filter(luyou='/tudilist/nadi', information_id=obj.id).count()
        elif obj.property_type == '2':
            count = ReceivePeo.objects.filter(luyou='/tudilist/gongdi', information_id=obj.id).count()

        elif obj.property_type == '3':
            count = ReceivePeo.objects.filter(luyou='/tudilist/shoulou', information_id=obj.id).count()

        else:
            count = ReceivePeo.objects.filter(luyou='/tudilist/loupan', information_id=obj.id).count()
        return count

    def get_shoucang(self, obj):
        if obj.property_type == '1':
            count = Collection.objects.filter(luyou='/tudilist/nadi', information_id=obj.id).count()
        elif obj.property_type == '2':
            count = Collection.objects.filter(luyou='/tudilist/gongdi', information_id=obj.id).count()

        elif obj.property_type == '3':
            count = Collection.objects.filter(luyou='/tudilist/shoulou', information_id=obj.id).count()

        else:
            count = Collection.objects.filter(luyou='/tudilist/loupan', information_id=obj.id).count()
        return count

    def get_xiazai(self, obj):
        if obj.property_type == '1':
            count = OrderInfo.objects.filter(luyou='/tudilist/nadi', land_id=obj.id).count()
        elif obj.property_type == '2':
            count = OrderInfo.objects.filter(luyou='/tudilist/gongdi', land_id=obj.id).count()

        elif obj.property_type == '3':
            count = OrderInfo.objects.filter(luyou='/tudilist/shoulou', land_id=obj.id).count()

        else:
            count = OrderInfo.objects.filter(luyou='/tudilist/loupan', land_id=obj.id).count()
        return count


class DealListSerializers(serializers.ModelSerializer):
    class Meta:
        model = LandInfo
        fields = ('id', 'city', 'create_on', 'area', 'location', 'serial_number', 'advance_date',
                  'transfer_date', 'land_nature', 'land_area', 'plot_ratio',
                  'transfer_mode', 'margin', 'start_price',
                  'transfer_high_price', 'plan_condition', 'deal_money', 'transferee_peo')


class InvChargeMergeListSerializers(serializers.ModelSerializer):
    is_file = serializers.SerializerMethodField()

    class Meta:
        model = InvChargeMerge
        fields = ('id', 'create_on', 'city', 'area', 'location', 'serial_number',
                  'land_nature', 'land_area', 'plot_ratio',
                  'building_density', 'trading_type', 'deposit', 'price', 'deal_money', 'transferee_peo',
                  'licensor', 'plan_conditions', 'trading_conditions', 'is_file', 'file_url')

    def get_is_file(self, obj):
        if obj.file_url:
            return True
        return False


class BuildingSupplyListSerializers(serializers.ModelSerializer):
    class Meta:
        model = BuildingSupplyF
        fields = ('id', 'create_on', 'city', 'acreage', 'tao_num', 'project_num',)


class BuildingSupplyTListSerializers(serializers.ModelSerializer):
    class Meta:
        model = BuildingSupplyT
        fields = ('id', 'create_on', 'city', 'acreage', 'tao_num', 'project_num',)


class ValueBuildingListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ValueBuilding
        fields = ('id', 'create_on', 'city', 'area', 'project_name', 'location',
                  'total_building_area', 'land_area', 'plot_ratio', 'total_tao',
                  'selling_tao', 'yitui_tao', 'in_average', 'selling_average',
                  'product_composition', 'h_area', 'supporting_business', 'supporting_education',
                  'traffic_conditions', 'developers', 'sales', 'first_time',)


class TopInListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Top_In
        fields = ('id', 'create_on', 'city', 'in_time', 'company_name', 'develop_project', 'new_ranking',
                  'headquarters_location',)


class BigDataListSerializers(serializers.ModelSerializer):
    is_file = serializers.SerializerMethodField()

    class Meta:
        model = BigData
        fields = (
            'id', 'create_on', 'city', 'positioning', 'city_card', 'GDP', 'peo_num', 'pillar_industries',
            'key_enterprises',
            'development_plan', 'planning_for', 'is_file', 'file_url')

    def get_is_file(self, obj):
        if obj.file_url:
            return True
        return False


# 公告邀请
class SelfLandInfoYaoqingTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    fabuzhe = serializers.SerializerMethodField()
    is_yaoqing_read = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = YaoQing
        fields = ('create_on', 'title', 'img', 'desc', 'fabuzhe', 'is_read', 'is_yaoqing_read', 'luyou', 'land_id', 'leibie')

    def get_title(self, obj):
        land_title = LandInfo.objects.filter(id=obj.land_id).first()
        return land_title.title

    def get_img(self, obj):
        land_img = LandInfo.objects.filter(id=obj.land_id).first()
        return land_img.img

    def get_desc(self, obj):
        land_title = LandInfo.objects.filter(id=obj.land_id).first()
        return land_title.desc

    def get_fabuzhe(self, obj):
        inv = ReleaseRecord.objects.filter(land_id=obj.land_id, luyou=obj.luyou).first()
        user = Users.objects.filter(id=inv.user_id).first()
        return user.username

    def get_is_read(self, obj):
        if ReceivePeo.objects.filter(user_id=obj.user_id, information_id=obj.land_id, luyou=obj.luyou):
            return True
        return False

    def get_is_yaoqing_read(self, obj):
        if YaoQingRead.objects.filter(user_id=obj.user_id, yaoqing_id=obj.id).first():
            return True
        return False

    def get_leibie(self, obj):
        if obj.luyou == '/tudimessage/nitui':
            return '拟推预告'
        elif obj.luyou == '/tudimessage/paimai':
            return '拍卖公告'
        elif obj.luyou == '/tudimessage/guapai':
            return '挂牌'
        elif obj.luyou == '/tudimessage/xiancheng':
            return '县城土地'
        else:
            return ''


# 公告收藏
class SelfLandInfoCollectionTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_contact = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ('create_on', 'title', 'is_contact', 'luyou', 'information_id')

    def get_title(self, obj):
        land_title = LandInfo.objects.filter(id=obj.information_id).first()
        return land_title.title

    def get_is_contact(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, land_id=obj.information_id, luyou=obj.luyou):
            return True
        return False


# 公告查看
class SelfLandInfoReceiveTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_contact = serializers.SerializerMethodField()

    class Meta:
        model = ReceivePeo
        fields = ('create_on', 'title', 'is_contact', 'luyou', 'information_id')

    def get_title(self, obj):
        land_title = LandInfo.objects.filter(id=obj.information_id).first()
        return land_title.title

    def get_is_contact(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, land_id=obj.information_id, luyou=obj.luyou):
            return True
        return False


# 挂牌公告查看
class SelfLandInfoGuapaiReceiveTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_collection = serializers.SerializerMethodField()

    class Meta:
        model = ReceivePeo
        fields = ('create_on', 'title', 'is_collection', 'luyou', 'information_id')

    def get_title(self, obj):
        land_title = LandInfo.objects.filter(id=obj.information_id).first()
        return land_title.title

    def get_is_collection(self, obj):
        if Collection.objects.filter(user_id=obj.user_id, information_id=obj.information_id).first():
            return True
        return False


# 公告联系
class SelfLandInfoContactTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    fabuer = serializers.SerializerMethodField()
    fabudanwei = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('create_on', 'title', 'fabuer', 'leibie', 'fabudanwei', 'luyou', 'land_id', 'mobile')

    def get_title(self, obj):
        land_title = LandInfo.objects.filter(id=obj.land_id).first()
        return land_title.title

    def get_fabuer(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.username

    def get_fabudanwei(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.company

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.mobile

    def get_leibie(self, obj):
        if obj.luyou == '/tudimessage/nitui':
            return '拟推预告'
        elif obj.luyou == '/tudimessage/paimai':
            return '拍卖公告'
        elif obj.luyou == '/tudimessage/guapai':
            return '挂牌'
        elif obj.luyou == '/tudimessage/xiancheng':
            return '县城土地'
        else:
            return ''


# 公告被联系
class SelfLandInfoContactedTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    maijia = serializers.SerializerMethodField()
    fabudanwei = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('create_on', 'title', 'maijia', 'fabudanwei', 'mobile', 'luyou', 'land_id', 'leibie')

    def get_title(self, obj):
        land_title = LandInfo.objects.filter(id=obj.land_id).first()
        return land_title.title

    def get_maijia(self, obj):
        # usered =
        user = Users.objects.filter(id=obj.user_id).first()
        return user.username

    def get_fabudanwei(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        return user.company

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        return user.mobile

    def get_leibie(self, obj):
        if obj.luyou == '/tudimessage/nitui':
            return '拟推预告'
        elif obj.luyou == '/tudimessage/paimai':
            return '拍卖公告'
        elif obj.luyou == '/tudimessage/guapai':
            return '挂牌'
        elif obj.luyou == '/tudimessage/xiancheng':
            return '县城土地'
        else:
            return ''

# 转让联系
class SelfTransInfoContactTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    fabuer = serializers.SerializerMethodField()
    fabudanwei = serializers.SerializerMethodField()
    ZC = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('create_on', 'title', 'fabuer', 'leibie', 'fabudanwei', 'luyou', 'land_id', 'ZC', 'mobile')

    def get_title(self, obj):
        land_title = TransInfo.objects.filter(id=obj.land_id).first()
        return land_title.title

    def get_fabuer(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.username

    def get_fabudanwei(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.company

    def get_leibie(self, obj):
        return '转让信息'

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.mobile

    def get_ZC(self, obj):
        z_c = Zan.objects.filter(user_id=self.context['user_id'], luyou=obj.luyou, land_id=obj.land_id).first()
        if z_c:
            return z_c.zc
        return '无'


# 转让被联系
class SelfTransInfoContactedTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    fabuer = serializers.SerializerMethodField()
    fabudanwei = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('create_on', 'title', 'fabuer', 'fabudanwei', 'mobile', 'luyou', 'land_id')

    def get_title(self, obj):
        land_title = TransInfo.objects.filter(id=obj.land_id).first()
        return land_title.title

    def get_fabuer(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        return user.username

    def get_fabudanwei(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        return user.company

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        return user.mobile


# 转让邀请
class SelfTransInfoYaoqingSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    fabuzhe = serializers.SerializerMethodField()
    is_yaoqing_read = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = YaoQing
        fields = ('create_on',  'fabuzhe', 'img', 'title', 'desc', 'is_read', 'is_yaoqing_read', 'luyou', 'land_id', 'leibie')

    def get_title(self, obj):
        land_title = TransInfo.objects.filter(id=obj.land_id).first()
        return land_title.title

    def get_img(self, obj):
        land_img = TransInfo.objects.filter(id=obj.land_id).first()
        return land_img.img

    def get_desc(self, obj):
        land_title = TransInfo.objects.filter(id=obj.land_id).first()
        return land_title.desc

    def get_fabuzhe(self, obj):
        inv = ReleaseRecord.objects.filter(land_id=obj.land_id, luyou=obj.luyou).first()
        user = Users.objects.filter(id=inv.user_id).first()
        return user.username

    def get_is_read(self, obj):
        if ReceivePeo.objects.filter(user_id=obj.user_id, information_id=obj.land_id, luyou=obj.luyou):
            return True
        return False

    def get_is_yaoqing_read(self, obj):
        if YaoQingRead.objects.filter(user_id=obj.user_id, yaoqing_id=obj.id).first():
            return True
        return False

    def get_leibie(self, obj):
        return '转让信息'


# 转让收藏
class SelfTransInfoCollectionSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_contact = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ('create_on', 'title', 'is_contact', 'luyou', 'information_id')

    def get_title(self, obj):
        land_title = TransInfo.objects.filter(id=obj.information_id).first()
        return land_title.title

    def get_is_contact(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, land_id=obj.information_id, luyou=obj.luyou):
            return True
        return False


# 转让查看
class SelfTransInfoReceiveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_contact = serializers.SerializerMethodField()

    class Meta:
        model = ReceivePeo
        fields = ('create_on', 'title', 'is_contact', 'luyou', 'information_id')

    def get_title(self, obj):
        land_title = TransInfo.objects.filter(id=obj.information_id).first()
        return land_title.title

    def get_is_contact(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, land_id=obj.information_id, luyou=obj.luyou):
            return True
        return False


# 转让的赞
class SelfTransInfoZanSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    fabuer = serializers.SerializerMethodField()

    class Meta:
        model = Zan
        fields = ('create_on', 'title', 'fabuer', 'luyou', 'land_id')

    def get_title(self, obj):
        land_title = TransInfo.objects.filter(id=obj.land_id).first()
        return land_title.title

    def get_fabuer(self, obj):
        trans_user = ReleaseRecord.objects.filter(land_id=obj.land_id, luyou=obj.luyou).first()
        user = Users.objects.filter(id=trans_user.user_id).first()
        return user.username


class SelfAttractInfoCollectionSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_contact = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ('create_on', 'title', 'is_contact', 'luyou', 'information_id')

    def get_title(self, obj):
        land_title = AttractInfo.objects.filter(id=obj.information_id).first()
        return land_title.title

    def get_is_contact(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, land_id=obj.information_id, luyou=obj.luyou):
            return True
        return False


class SelfAttractInfoReceiveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_contact = serializers.SerializerMethodField()

    class Meta:
        model = ReceivePeo
        fields = ('create_on', 'title', 'is_contact', 'luyou', 'information_id')

    def get_title(self, obj):
        land_title = AttractInfo.objects.filter(id=obj.information_id).first()
        return land_title.title

    def get_is_contact(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, land_id=obj.information_id, luyou=obj.luyou):
            return True
        return False


# 招商邀请
class SelfAttractYaoqingSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    fabuzhe = serializers.SerializerMethodField()
    is_yaoqing_read = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = YaoQing
        fields = ('create_on', 'title', 'img', 'desc', 'fabuzhe', 'is_read', 'is_yaoqing_read', 'luyou', 'land_id', 'leibie')

    def get_title(self, obj):
        land_title = AttractInfo.objects.filter(id=obj.land_id).first()
        return land_title.title

    def get_img(self, obj):
        land_img = AttractInfo.objects.filter(id=obj.land_id).first()
        return land_img.img

    def get_desc(self, obj):
        land_title = AttractInfo.objects.filter(id=obj.land_id).first()
        return land_title.desc

    def get_fabuzhe(self, obj):
        inv = ReleaseRecord.objects.filter(land_id=obj.land_id, luyou=obj.luyou).first()
        user = Users.objects.filter(id=inv.user_id).first()
        return user.username

    def get_is_read(self, obj):
        if ReceivePeo.objects.filter(user_id=obj.user_id, information_id=obj.land_id, luyou=obj.luyou):
            return True
        return False

    def get_is_yaoqing_read(self, obj):
        if YaoQingRead.objects.filter(user_id=obj.user_id, yaoqing_id=obj.id).first():
            return True
        return False

    def get_leibie(self, obj):
        return '招商信息'


# 招商联系
class SelfAttractContactTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    fabuer = serializers.SerializerMethodField()
    fabudanwei = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('create_on', 'title', 'fabuer', 'leibie', 'fabudanwei', 'luyou', 'land_id', 'mobile')

    def get_title(self, obj):
        land_title = AttractInfo.objects.filter(id=obj.land_id).first()
        if land_title:
            return land_title.title
        return ''

    def get_fabuer(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.username

    def get_fabudanwei(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.company

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.contacted_id).first()
        return user.mobile

    def get_leibie(self, obj):
        return '招商信息'


# 招商被联系
class SelfAttractContactedTableSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    fabuer = serializers.SerializerMethodField()
    fabudanwei = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('create_on', 'title', 'leibie', 'fabuer', 'fabudanwei', 'mobile', 'luyou', 'land_id')

    def get_title(self, obj):
        land_title = AttractInfo.objects.filter(id=obj.land_id).first()
        if land_title:
            return land_title.title
        return ''

    def get_fabuer(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        return user.username

    def get_fabudanwei(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        return user.company

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        return user.mobile

    def get_leibie(self, obj):
        return '招商信息'


# 活动邀请
class ActivityYaoqingSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    fabuzhe = serializers.SerializerMethodField()
    is_yaoqing_read = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = YaoQing
        fields = ('title', 'is_read', 'img', 'is_yaoqing_read', 'desc', 'fabuzhe', 'create_on', 'luyou', 'land_id', 'leibie')

    def get_title(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        activity = Activity.objects.filter(id=obj.land_id).first()
        return activity.title

    def get_img(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        activity = Activity.objects.filter(id=obj.land_id).first()
        return activity.img

    def get_fabuzhe(self, obj):
        inv = ReleaseRecord.objects.filter(land_id=obj.land_id, luyou=obj.luyou).first()
        user = Users.objects.filter(id=inv.user_id).first()
        return user.username

    def get_desc(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        activity = Activity.objects.filter(id=obj.land_id).first()
        return activity.desc

    def get_is_read(self, obj):
        if ReceivePeo.objects.filter(user_id=obj.user_id, information_id=obj.land_id, luyou=obj.luyou).first():
            return True
        return False

    def get_is_yaoqing_read(self, obj):
        if YaoQingRead.objects.filter(user_id=obj.user_id, yaoqing_id=obj.id).first():
            return True
        return False

    def get_leibie(self, obj):
        if obj.luyou == '/activity/shalong':
            return '沙龙活动'
        elif obj.luyou == '/activity/yuebao':
            return '月报活动'
        elif obj.luyou == '/activity/tuijie':
            return '推介会'
        elif obj.luyou == '/activity/kuanian':
            return '跨年活动'


# 活动查看
class ActivityReceiveSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_collection = serializers.SerializerMethodField()

    class Meta:
        model = ReceivePeo
        fields = ('id', 'title', 'is_collection', 'create_on', 'luyou', 'information_id')

    def get_title(self, obj):
        activity = Activity.objects.filter(id=obj.information_id).first()
        return activity.title

    def get_is_collection(self, obj):
        if Collection.objects.filter(user_id=obj.user_id, information_id=obj.information_id).first():
            return True
        return False


# 活动报名
class ActivitySingUpSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    additional = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()

    class Meta:
        model = OrderInfo
        fields = ('title', 'order_mount', 'pay_time', 'leibie', 'luyou', 'land_id', 'additional')

    def get_title(self, obj):
        activity = Activity.objects.filter(id=obj.land_id).first()
        return activity.title

    def get_additional(self, obj):
        activity = Activity.objects.filter(id=obj.land_id).first()
        return activity.additional

    def get_is_collection(self, obj):
        if Collection.objects.filter(user_id=obj.user_id, information_id=obj.land_id).first():
            return True
        return False

    def get_leibie(self, obj):
        if obj.luyou == '/activity/shalong':
            return '沙龙活动'
        elif obj.luyou == '/activity/yuebao':
            return '月报活动'
        elif obj.luyou == '/activity/tuijie':
            return '推介会'
        elif obj.luyou == '/activity/kuanian':
            return '跨年活动'


# 活动收藏
class ActivityCollectionSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_sign_up = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ('title', 'create_on', 'is_sign_up', 'luyou', 'information_id')

    def get_title(self, obj):
        activity = Activity.objects.filter(id=obj.information_id).first()
        return activity.title

    def get_is_sign_up(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, luyou=obj.luyou, land_id=obj.information_id).first():
            return True
        return False


# 榜单接收
class PropertyListYaoqingSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    fabuzhe = serializers.SerializerMethodField()
    is_yaoqing_read = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = YaoQing
        fields = ('title', 'is_read', 'img', 'is_yaoqing_read', 'desc', 'fabuzhe','create_on', 'luyou', 'land_id', 'leibie')

    def get_title(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        proper = PropertyList.objects.filter(id=obj.land_id).first()
        return proper.title

    def get_img(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        proper = PropertyList.objects.filter(id=obj.land_id).first()
        return proper.img

    def get_fabuzhe(self, obj):
        inv = ReleaseRecord.objects.filter(land_id=obj.land_id, luyou=obj.luyou).first()
        user = Users.objects.filter(id=inv.user_id).first()
        return user.username

    def get_desc(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        proper = PropertyList.objects.filter(id=obj.land_id).first()
        return proper.desc

    def get_is_read(self, obj):
        if ReceivePeo.objects.filter(user_id=obj.user_id, information_id=obj.land_id, luyou=obj.luyou).first():
            return True
        return False

    def get_is_yaoqing_read(self, obj):
        if YaoQingRead.objects.filter(user_id=obj.user_id, yaoqing_id=obj.id).first():
            return True
        return False

    def get_leibie(self, obj):
        if obj.luyou == "/tudilist/nadi":
            return '企业拿地榜'
        elif obj.luyou == "/tudilist/gongdi":
            return '城市供地榜'
        elif obj.luyou == "/tudilist/shoulou":
            return '楼市榜'
        elif obj.luyou == "/tudilist/loupan":
            return '楼盘榜'


# 榜单下载
class PropertyListDownSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()

    class Meta:
        model = OrderInfo
        fields = ('title', 'order_mount', 'leibie', 'pay_time', 'luyou', 'land_id')

    def get_title(self, obj):
        proper = PropertyList.objects.filter(id=obj.land_id).first()
        return proper.title

    def get_leibie(self, obj):
        if obj.luyou == "/tudilist/nadi":
            return '企业拿地榜'
        elif obj.luyou == "/tudilist/gongdi":
            return '城市供地榜'
        elif obj.luyou == "/tudilist/shoulou":
            return '楼市榜'
        elif obj.luyou == "/tudilist/loupan":
            return '楼盘榜'


# 榜单收藏
class PropertyListCollectionSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_down = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ('title', 'create_on', 'is_down', 'luyou', 'information_id')

    def get_title(self, obj):
        property = PropertyList.objects.filter(id=obj.information_id).first()
        return property.title

    def get_is_down(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, luyou=obj.luyou, land_id=obj.information_id).first():
            return True
        return False


# 榜单查看
class PropertyListReceiveSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_collection = serializers.SerializerMethodField()

    class Meta:
        model = ReceivePeo
        fields = ('id', 'title', 'is_collection', 'create_on', 'luyou', 'information_id')

    def get_title(self, obj):
        property = PropertyList.objects.filter(id=obj.information_id).first()
        return property.title

    def get_is_collection(self, obj):
        if Collection.objects.filter(user_id=obj.user_id, information_id=obj.information_id).first():
            return True
        return False


# 数据接收
class InvestmentDataYaoqingSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    fabuzhe = serializers.SerializerMethodField()
    is_yaoqing_read = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    class Meta:
        model = YaoQing
        fields = ('title', 'is_read', 'is_yaoqing_read', 'img', 'desc', 'fabuzhe','create_on', 'luyou', 'land_id', 'leibie')

    def get_title(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        inv = InvestmentData.objects.filter(id=obj.land_id).first()
        return inv.title

    def get_img(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        inv = InvestmentData.objects.filter(id=obj.land_id).first()
        return inv.img

    def get_fabuzhe(self, obj):
        inv = ReleaseRecord.objects.filter(land_id=obj.land_id, luyou=obj.luyou).first()
        user = Users.objects.filter(id=inv.user_id).first()
        return user.username

    def get_desc(self, obj):
        # timrs = obj.activity_datetime.split('T')[0]
        # a = timrs.replace(timrs[-1], str(int(timrs[-1]) + 1))
        inv = InvestmentData.objects.filter(id=obj.land_id).first()
        return inv.desc

    def get_is_read(self, obj):
        if ReceivePeo.objects.filter(user_id=obj.user_id, information_id=obj.land_id, luyou=obj.luyou).first():
            return True
        return False

    def get_is_yaoqing_read(self, obj):
        if YaoQingRead.objects.filter(user_id=obj.user_id, yaoqing_id=obj.id).first():
            return True
        return False

    def get_leibie(self, obj):
        if obj.luyou == "/Investment/zhoubao":
            return '周报'
        elif obj.luyou == "/Investment/yuebao":
            return '月报'
        elif obj.luyou == "/Investment/jibao":
            return '季报'
        elif obj.luyou == "/Investment/bannianbao":
            return '半年报'
        elif obj.luyou == "/Investment/nianbao":
            return '年报'


# 数据下载
class InvestmentDataDownSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    leibie = serializers.SerializerMethodField()

    class Meta:
        model = OrderInfo
        fields = ('title', 'order_mount', 'pay_time', 'leibie', 'luyou', 'land_id')

    def get_title(self, obj):
        inv = InvestmentData.objects.filter(id=obj.land_id).first()
        return inv.title

    def get_leibie(self, obj):
        if obj.luyou == "/Investment/zhoubao":
            return '周报'
        elif obj.luyou == "/Investment/yuebao":
            return '月报'
        elif obj.luyou == "/Investment/jibao":
            return '季报'
        elif obj.luyou == "/Investment/bannianbao":
            return '半年报'
        elif obj.luyou == "/Investment/nianbao":
            return '年报'


# 数据收藏
class InvestmentDataCollectionSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_down = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ('title', 'create_on', 'is_down', 'luyou', 'information_id')

    def get_title(self, obj):
        property = InvestmentData.objects.filter(id=obj.information_id).first()
        return property.title

    def get_is_down(self, obj):
        if OrderInfo.objects.filter(user_id=obj.user_id, luyou=obj.luyou, land_id=obj.information_id).first():
            return True
        return False


# 数据查看
class InvestmentDataReceiveSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    is_collection = serializers.SerializerMethodField()

    class Meta:
        model = ReceivePeo
        fields = ('title', 'create_on', 'is_collection', 'luyou', 'information_id')

    def get_title(self, obj):
        property = InvestmentData.objects.filter(id=obj.information_id).first()
        return property.title

    def get_is_collection(self, obj):
        if Collection.objects.filter(user_id=obj.user_id, information_id=obj.information_id).first():
            return True
        return False


class ReleaseRecordListSerializers(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    create_on = serializers.SerializerMethodField()
    receive_peo = serializers.SerializerMethodField()
    collection = serializers.SerializerMethodField()
    contact_ed = serializers.SerializerMethodField()
    zan = serializers.SerializerMethodField()
    cai = serializers.SerializerMethodField()
    audit_state = serializers.SerializerMethodField()
    shouru = serializers.SerializerMethodField()
    yaoqing = serializers.SerializerMethodField()

    class Meta:
        model = ReleaseRecord
        fields = (
            'title', 'create_on', 'yaoqing', 'receive_peo', 'collection', 'contact_ed', 'zan', 'cai', 'audit_state',
            'shouru', 'luyou', 'land_id')

    def get_title(self, obj):
        if obj.luyou == '/tudimessage/zhuanrang':
            land = TransInfo.objects.filter(id=obj.land_id).first()
            return land.title
        elif obj.luyou == '/tudimessage/zhaoshang':
            land = AttractInfo.objects.filter(id=obj.land_id).first()
            return land.title
        else:
            land = LandInfo.objects.filter(id=obj.land_id).first()
            return land.title

    def get_create_on(self, obj):
        if obj.luyou == '/tudimessage/zhuanrang':
            land = TransInfo.objects.filter(id=obj.land_id).first()
            return land.create_on
        elif obj.luyou == '/tudimessage/zhaoshang':
            land = AttractInfo.objects.filter(id=obj.land_id).first()
            return land.create_on
        else:
            land = LandInfo.objects.filter(id=obj.land_id).first()
            return land.create_on

    def get_yaoqing(self, obj):
        user_id = self.context['user_id']
        return YaoQing.objects.filter(yaoqingren=user_id, land_id=obj.land_id).count()

    def get_receive_peo(self, obj):
        return ReceivePeo.objects.filter(luyou=obj.luyou, information_id=obj.land_id).count()

    def get_collection(self, obj):
        return Collection.objects.filter(luyou=obj.luyou, information_id=obj.land_id).count()

    def get_contact_ed(self, obj):
        user_id = self.context['user_id']
        return Contact.objects.filter(luyou=obj.luyou, land_id=obj.land_id, contacted_id=user_id).count()

    def get_zan(self, obj):
        if obj.luyou == '/tudimessage/zhuanrang':
            return Zan.objects.filter(land_id=obj.land_id, zc=1).count()
        return '无'

    def get_cai(self, obj):
        if obj.luyou == '/tudimessage/zhuanrang':
            return Zan.objects.filter(land_id=obj.land_id, zc=2).count()
        return '无'

    def get_audit_state(self, obj):
        if obj.luyou == '/tudimessage/zhuanrang':
            land = TransInfo.objects.filter(id=obj.land_id).first()
            return land.audit_state
        elif obj.luyou == '/tudimessage/zhaoshang':
            land = AttractInfo.objects.filter(id=obj.land_id).first()
            return land.audit_state
        else:
            land = LandInfo.objects.filter(id=obj.land_id).first()
            return land.audit_state

    def get_shouru(self, obj):
        user_id = self.context['user_id']
        return 99.5 * Contact.objects.filter(luyou=obj.luyou, land_id=obj.land_id, contacted_id=user_id).count()


# 剩余可查看条数
class ChargeNumberSerializers(serializers.ModelSerializer):
    class Meta:
        model = ChargeNumber
        fields = ('nitui', 'paimai', 'zhuanrang', 'zhaoshang', 'xiancheng', 'shalong', 'yuebao', 'nadi', 'gongdi'
                  , 'shoufang', 'loupan', 'yuebaodata', 'zhoubao', 'jibao')


class ConsumptionSerializers(serializers.ModelSerializer):
    leibie = serializers.SerializerMethodField()

    class Meta:
        model = OrderInfo
        fields = ('land_id', 'pay_time', 'subject', 'leibie', 'order_mount', 'luyou',)

    def get_leibie(self, obj):
        if obj.luyou in ['/tudimessage/nitui', '/tudimessage/paimai', '/tudimessage/guapai', '/tudimessage/zhuanrang',
                         '/tudimessage/zhaoshang', '/tudimessage/xiancheng']:
            leibie = '土地信息'
            return leibie
        elif obj.luyou in ['/activity/shalong', '/activity/yuebao', '/activity/tuijie', '/activity/kuanian']:
            leibie = '找地活动'
            return leibie
        elif obj.luyou in ["/tudilist/nadi", "/tudilist/gongdi", "/tudilist/shoulou", "/tudilist/loupan"]:
            leibie = '地产榜单'
            return leibie
        elif obj.luyou in ["/Investment/zhoubao", "/Investment/yuebao", "/Investment/jibao", "/Investment/bannnianbao",
                           "/Investment/nianbao"]:
            leibie = '投资数据'
            return leibie
        else:
            leibie = '会员充值'
            return leibie


class FaBuYaoqingSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = YaoQing
        fields = ('create_on', 'username', 'company', 'mobile')

    def get_username(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.username
        return ''

    def get_company(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.company
        return ''

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.mobile
        return ''


class FaBuChakanSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = ReceivePeo
        fields = ('create_on', 'username', 'company', 'mobile')

    def get_username(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.username
        return ''

    def get_company(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.company
        return ''

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.mobile
        return ''

class FaBuShoucangSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ('create_on', 'username', 'company', 'mobile')

    def get_username(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.username
        return ''

    def get_company(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.company
        return ''

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.mobile
        return ''


class FaBuLianxiSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('create_on', 'username', 'company', 'mobile')

    def get_username(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.username
        return ''

    def get_company(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.company
        return ''

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.mobile
        return ''


class FaBuZanSerializers(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = Zan
        fields = ('create_on', 'username', 'company', 'mobile')

    def get_username(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.username
        return ''

    def get_company(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.company
        return ''

    def get_mobile(self, obj):
        user = Users.objects.filter(id=obj.user_id).first()
        if user:
            return user.mobile
        return ''


class ClientLandSerializers(serializers.ModelSerializer):
    opinion = serializers.SerializerMethodField()

    class Meta:
        model = LandInfo
        fields = ('id', 'city', 'create_on', 'area', 'location', 'serial_number', 'land_type', 'advance_date',
                  'listed_date', 'transfer_date', 'land_nature', 'land_area', 'plot_ratio', 'c_f', 'reward_price',
                  'transfer_mode', 'margin', 'start_price', 'remark', 'greening', 'building_density', 'img_list',
                  'transfer_high_price', 'plan_condition', 'file_url', 'yuji_guapai', 'now_progress', 'add_amplitude','pcc',
                  'special_requirements', 'title', 'desc', 'img', 'content', 'create_on', 'opinion', 'house_account','coordinates')

    def get_opinion(self, obj):
        opinion = AuditOpinion.objects.filter(land_id=obj.id, source='land').first()
        if opinion:
            return opinion.opinion
        else:
            return ''


class ClientTransSerializers(serializers.ModelSerializer):
    opinion = serializers.SerializerMethodField()

    class Meta:
        model = TransInfo
        fields = ('id', 'create_on', 'city', 'area', 'location', 'serial_number',
                  'land_nature', 'land_area', 'plot_ratio', 'greening',
                  'building_density', 'trading_type', 'deposit', 'price', 'reward_price',
                  'people', 'contact', 'plan_conditions', 'licensor', 'trading_conditions',
                  'file_url', 'img_list', 'information_validity', 'remark','pcc',
                  'title', 'desc', 'img', 'content', 'create_on', 'opinion', 'house_account','coordinates'
                  )

    def get_opinion(self, obj):
        opinion = AuditOpinion.objects.filter(land_id=obj.id, source='trans').first()
        if opinion:
            return opinion.opinion
        else:
            return ''


class ClientAttractSerializers(serializers.ModelSerializer):
    opinion = serializers.SerializerMethodField()

    class Meta:
        model = AttractInfo
        fields = ('id', 'create_on', 'city', 'area', 'location', 'serial_number',
                  'land_nature', 'land_area', 'plot_ratio', 'reward_price',
                  'notice_date', 'total_inv', 'img_list', 'industry_requirements',
                  'people', 'contact', 'cooperate_condition', 'file_url', 'remark','pcc',
                  'title', 'desc', 'img', 'content', 'create_on', 'opinion', 'house_account','coordinates'
                  )

    def get_opinion(self, obj):
        opinion = AuditOpinion.objects.filter(land_id=obj.id, source='attract').first()
        if opinion:
            return opinion.opinion
        else:
            return ''


class ClientActivitySerializers(serializers.ModelSerializer):
    opinion = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'activity_datetime', 'activity_place', 'information_source',
            'reward_price', 'create_on', 'traffic_tips', 'content_feed', 'audit_state')

    def get_opinion(self, obj):
        opinion = AuditOpinion.objects.filter(land_id=obj.id, source='activity').first()
        if opinion:
            return opinion.opinion
        else:
            return ''


class ClientPopListSerializers(serializers.ModelSerializer):
    opinion = serializers.SerializerMethodField()

    class Meta:
        model = PropertyList
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'reward_price', 'information_source', 'create_on',
            'information_source', 'file_introduction', 'file_url', 'audit_state')

    def get_opinion(self, obj):
        opinion = AuditOpinion.objects.filter(land_id=obj.id, source='poplist').first()
        if opinion:
            return opinion.opinion
        else:
            return ''


class ClientInvestmentDataSerializers(serializers.ModelSerializer):
    opinion = serializers.SerializerMethodField()

    class Meta:
        model = InvestmentData
        fields = (
            'id', 'title', 'desc', 'img', 'content', 'reward_price', 'information_source', 'create_on',
            'information_source', 'file_introduction', 'file_url', 'audit_state')

    def get_opinion(self, obj):
        opinion = AuditOpinion.objects.filter(land_id=obj.id, source='poplist').first()
        if opinion:
            return opinion.opinion
        else:
            return ''
