from django.db import models
from apps.user.models import Users

# Create your models here.
"""
1公开市场土地供应头部汇总：挂牌公告、预告.拍卖公告、县城土地
公开市场土地供应表格字段：录入日期、数据类别、序号、城市、区、位置、编号、用地面积、容积率、用地性质、规划条件、挂牌文件、出让方式、保证金，起始价，出让最高价，预告日期、挂牌日期、出让日期


"""
# TODO: null=True,数据库中的数据为空 blank=True： 表单提交可以为空


class LandInfo(models.Model):  # 土地信息
    # 价格类字段说明:
    # margin,start_price,transfer_high_price 万元单位
    data_type_choice = ((1, '挂牌公告'), (2, '拟推预告'), (3, '拍卖公告'), (4, '县城土地'))
    desc = models.CharField('简介', max_length=400, default='', null=True, blank=True)
    title = models.CharField('标题', max_length=100, default='', null=True, blank=True)
    create_on = models.DateField('录入日期', auto_now_add=True)
    land_type = models.CharField('数据类别', choices=data_type_choice, max_length=2)
    city = models.CharField('城市', max_length=200, default='')
    area = models.CharField('区', max_length=200, default='')
    location = models.CharField('位置', max_length=500, default='')
    serial_number = models.CharField('编号', max_length=200, default='')
    land_area = models.FloatField('用地面积', null=True, blank=True)
    plot_ratio = models.FloatField('容积率', null=True, blank=True)
    greening = models.FloatField('绿化率', null=True, blank=True)
    building_density = models.FloatField('建筑密度', null=True, blank=True)
    land_nature = models.CharField(verbose_name='用地性质', max_length=100, default='')
    plan_condition = models.TextField(verbose_name='规划条件', null=True, blank=True)
    transfer_mode = models.CharField(verbose_name='出让方式', max_length=200, default='')
    house_account = models.CharField('住房比', max_length=64, default='',null=True)
    file_url = models.CharField('文件路径', null=True, blank=True, max_length=32)
    margin = models.FloatField(verbose_name='保证金', default=0)  # 以万元单位
    start_price = models.FloatField(verbose_name='起始价', default=0, null=True, blank=True)  # 以万元单位
    transfer_high_price = models.FloatField(verbose_name='出让最高价', null=True, blank=True)  # 以万元单位
    advance_date = models.CharField(verbose_name='预告日期', max_length=50, default='')
    listed_date = models.CharField(verbose_name='挂牌日期', max_length=50, default='')
    transfer_date = models.CharField(verbose_name='出让日期', max_length=50, default='')
    remark = models.CharField('备注', max_length=200, null=True, blank=True)
    c_f = models.CharField('撤牌或者复牌', max_length=32, null=True, blank=True)
    information_source = models.CharField(verbose_name='信息来源', max_length=200, default='')
    img = models.CharField('图片', max_length=100, default='', null=True)
    content = models.TextField(verbose_name='详细内容', default='', null=True, blank=True)
    views_number = models.IntegerField(verbose_name='查看次数', null=True, blank=True, default=0)
    reward_price = models.FloatField(verbose_name='价格', default=0.01, null=True, blank=True)
    is_publish = models.IntegerField('是否已发布', default=0)
    is_deal = models.IntegerField('是否成交', default=0)
    deal_time = models.CharField('成交时间', default='', max_length=32)
    deal_money = models.FloatField('成交金额', default=0)
    transferee_peo = models.CharField('受让人', default='', max_length=32)
    deal_remark = models.CharField('备注', default='', max_length=64)
    audit_state = models.IntegerField(default=0)
    img_list = models.CharField('图集', max_length=500, default='')
    yuji_guapai = models.CharField('预计挂牌时间', max_length=128, default='', null=True, blank=True)
    now_progress = models.CharField('目前进度', max_length=128, default='', null=True, blank=True)
    add_amplitude = models.CharField('加价幅度', default='', max_length=32, null=True, blank=True)
    special_requirements = models.CharField('特殊要求', max_length=256, default='', null=True, blank=True)
    coordinates = models.TextField('坐标', default='', null=True, blank=True)
    pcc = models.CharField('省市县坐标', default='', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = '土地信息'
        verbose_name_plural = verbose_name


"""
2转让信息头部汇总：转让信息
转让信息表格字段：录入日期、序号、城市、区、编号、位置、用地性质、用地面积、容积率、建筑密度、交易模式、定金、报价、交易条件、规划条件、联系人、联系方式、出让方


"""


class TransInfo(models.Model):  # 转让信息
    create_on = models.DateField(verbose_name='录入日期', auto_now_add=True)
    title = models.CharField('标题', max_length=100, default='', null=True, blank=True)
    desc = models.CharField('简介', max_length=400, default='', null=True, blank=True)
    city = models.CharField(verbose_name='城市', max_length=200, default='')
    area = models.CharField(verbose_name='区', max_length=200, default='')
    location = models.CharField(verbose_name='位置', max_length=200, default='')
    serial_number = models.CharField(verbose_name='编号', max_length=200, default='')
    land_nature = models.CharField(verbose_name='用地性质', max_length=100, default='')
    land_area = models.FloatField(verbose_name='面积', default=0)
    plot_ratio = models.FloatField(verbose_name='容积率', default=0)
    greening = models.FloatField('绿化率', default=0)
    building_density = models.FloatField('建筑密度', null=True, blank=True)
    trading_type = models.CharField(verbose_name='交易模式', max_length=50, default='')
    deposit = models.FloatField(verbose_name='定金', default=0)
    price = models.FloatField(verbose_name='报价', default=0)
    house_account = models.CharField('住房比', max_length=64, default='',null=True)
    trading_conditions = models.CharField(verbose_name='交易条件', default='', max_length=200)
    plan_conditions = models.CharField(verbose_name='规划条件', default='', max_length=200)
    people = models.CharField(verbose_name='联系人', max_length=20, default='')
    contact = models.CharField(verbose_name='联系方式', max_length=20, default='')
    licensor = models.CharField(verbose_name='出让方', max_length=64, default='')
    information_source = models.CharField(verbose_name='信息来源', max_length=200)
    img = models.CharField('图片', max_length=100, default='', null=True, blank=True)
    content = models.TextField(verbose_name='详细内容', default='', null=True, blank=True)
    views_number = models.IntegerField(verbose_name='查看次数', null=True, blank=True, default=0)
    reward_price = models.FloatField(verbose_name='价格', default=0.01)
    file_url = models.CharField('文件路径', null=True, blank=True, max_length=32)
    audit_state = models.IntegerField(default=0)
    img_list = models.CharField('图集', max_length=500, default='')
    information_validity = models.CharField('信息有效期', max_length=32, default='', null=True, blank=True)
    remark = models.CharField('备注', max_length=256, default='', null=True, blank=True)
    coordinates = models.TextField('坐标', default='', null=True, blank=True)
    pcc = models.CharField('省市县坐标', default='', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = '转让信息'
        verbose_name_plural = verbose_name


"""
3招商信息头部汇总：招商信息
招商信息表格字段：录入日期、序号，城市，区，编号，位置，用地性质，用地面积，合作条件，总投资额，公告日期，联系人，联系方式


"""


class AttractInfo(models.Model):  # 招商信息
    create_on = models.DateField(verbose_name='录入日期', auto_now_add=True)
    title = models.CharField('标题', max_length=100, default='', null=True, blank=True)
    desc = models.CharField('简介', max_length=400, default='', null=True, blank=True)
    city = models.CharField(verbose_name='城市', max_length=200, default='')
    area = models.CharField(verbose_name='区', max_length=200, default='')
    serial_number = models.CharField(verbose_name='编号', max_length=200, default='')
    location = models.CharField(verbose_name='位置', max_length=500, default='')
    land_nature = models.CharField(verbose_name='用地性质', max_length=100, default='')
    house_account = models.CharField('住房比', max_length=64, default='',null=True)
    land_area = models.FloatField(verbose_name='用地面积', default=0)
    cooperate_condition = models.CharField(verbose_name='合作条件', default='', max_length=200, null=True, blank=True)
    total_inv = models.FloatField(verbose_name='总投资额', default=0)  # 100亿上限，万元单位
    notice_date = models.CharField(verbose_name='公告日期', max_length=32, null=True, blank=True)
    people = models.CharField(verbose_name='联系人', max_length=200, default='')
    contact = models.CharField(verbose_name='联系方式', max_length=20, default='')
    file_url = models.CharField('文件路径', null=True, blank=True, max_length=32)
    plot_ratio = models.FloatField(verbose_name='容积率', default=0)
    information_source = models.CharField(verbose_name='信息来源', max_length=200, default='', null=True, blank=True)
    img = models.CharField('图片', max_length=32, default='', null=True, blank=True)
    content = models.TextField(verbose_name='详细内容', default='', null=True, blank=True)
    views_number = models.IntegerField(verbose_name='查看次数', null=True, blank=True, default=0)
    reward_price = models.FloatField(verbose_name='价格', default=0.01)
    audit_state = models.IntegerField(default=0)
    img_list = models.CharField('图集', max_length=500, default='', null=True, blank=True)
    industry_requirements = models.CharField('产业要求', max_length=128, default='', null=True, blank=True)
    remark = models.CharField('备注', max_length=256, default='', null=True, blank=True)
    coordinates = models.TextField('坐标', default='', null=True, blank=True)
    pcc = models.CharField('省市县坐标', default='', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = '招商信息'
        verbose_name_plural = verbose_name


ACTIVITY_TYPE_CHOICES = (
    (1, '沙龙'),
    (2, '月报'),
    (3, '推荐会'),
    (4, '跨年')
)


class Activity(models.Model):
    # 找地活动
    activity_type = models.CharField('活动类型', choices=ACTIVITY_TYPE_CHOICES, max_length=2, default='')
    city = models.CharField(verbose_name='城市', max_length=200, default='')
    title = models.CharField('标题', max_length=100, default='')
    desc = models.CharField('简介', max_length=400, default='')
    area = models.CharField(verbose_name='区', max_length=200, default='')
    location = models.CharField(verbose_name='位置', max_length=500, default='')
    serial_number = models.CharField(verbose_name='编号', max_length=200, default='')
    land_area = models.FloatField(verbose_name='用地面积', default=0)
    plot_ratio = models.FloatField(verbose_name='容积率', default=0)
    land_nature = models.CharField(verbose_name='用地性质', max_length=100, default='')
    create_on = models.DateField(verbose_name='发布日期', auto_now_add=True)
    information_source = models.CharField(verbose_name='信息来源', max_length=200, default='')
    img = models.CharField('图片', max_length=100, default='')
    content = models.TextField(verbose_name='详细内容', default='')
    views_number = models.IntegerField(verbose_name='查看次数', default=0)
    reward_price = models.FloatField(verbose_name='价格', default=0)
    activity_datetime = models.CharField(verbose_name='活动时间', max_length=200, default='')
    activity_place = models.CharField(verbose_name='活动地点', max_length=300, default='')
    quota = models.IntegerField(verbose_name='名额', default=0)
    additional = models.CharField('附加权益', max_length=32, default='')
    traffic_tips = models.CharField('交通提示', max_length=256, default='')
    content_feed = models.TextField('内容提要', default='')

    audit_state = models.IntegerField('审核状态', default=0,)

    class Meta:
        verbose_name = '找地活动'
        verbose_name_plural = verbose_name


PROPERTY_TYPE_CHOICES = (
    (1, '企业拿地榜'),
    (2, '城市供地榜'),
    (3, '城市售楼榜'),
    (4, '价值楼盘榜')
)


class PropertyList(models.Model):
    # 地产榜单咨询表
    title = models.CharField('标题', max_length=100, default='')
    desc = models.CharField('简介', max_length=400, default='')
    information_source = models.CharField(verbose_name='信息来源', max_length=200, default='')
    img = models.CharField('图片', max_length=100, default='')
    content = models.TextField(verbose_name='详细内容', default='')
    property_type = models.CharField('活动类型', choices=ACTIVITY_TYPE_CHOICES, max_length=2, default=1)
    reward_price = models.FloatField(verbose_name='价格', default=0)
    create_on = models.DateField(verbose_name='发布日期', auto_now_add=True)
    views_number = models.IntegerField(verbose_name='查看次数', null=True, blank=True, default=0)
    audit_state = models.IntegerField('审核状态', default=0,)

    file_introduction = models.CharField('文件简介', max_length=256, default='')
    file_url = models.CharField('文件路径', null=True, blank=True, max_length=32)


INVESTMENT_TYPE_CHOICES = (
    (1, '周报'),
    (2, '月报'),
    (3, '季报'),
    (4, '半年报'),
    (5, '年报')
)


class InvestmentData(models.Model):
    # 投资数据咨询表
    title = models.CharField('标题', max_length=100, default='')
    desc = models.CharField('简介', max_length=400, default='')
    information_source = models.CharField(verbose_name='信息来源', max_length=200, default='')
    img = models.CharField('图片', max_length=100, default='')
    content = models.TextField(verbose_name='详细内容', default='')
    property_type = models.CharField('活动类型', choices=INVESTMENT_TYPE_CHOICES, max_length=2, default=1)
    reward_price = models.FloatField(verbose_name='价格', default=0)
    create_on = models.DateField(verbose_name='发布日期', auto_now_add=True)
    views_number = models.IntegerField(verbose_name='查看次数', null=True, blank=True, default=0)
    file_introduction = models.CharField('文件简介', max_length=256, default='')
    file_url = models.CharField('文件路径', null=True, blank=True, max_length=32)
    audit_state = models.IntegerField('审核状态', default=0,)


class InvChargeMerge(models.Model):
    # 投资数据 录入 收并购表
    create_on = models.DateField('创建时间', auto_now_add=True)
    city = models.CharField(verbose_name='城市', max_length=200, default='')
    area = models.CharField(verbose_name='区', max_length=200, default='')
    serial_number = models.CharField(verbose_name='编号', max_length=200, default='')
    location = models.CharField(verbose_name='位置', max_length=500, default='')
    land_nature = models.CharField(verbose_name='用地性质', max_length=100, default='')
    land_area = models.FloatField(verbose_name='用地面积', default=0)
    plot_ratio = models.FloatField(verbose_name='容积率', default=0)
    building_density = models.FloatField('建筑密度', null=True, blank=True)
    trading_type = models.CharField(verbose_name='交易模式', max_length=50, default='')
    deposit = models.FloatField(verbose_name='定金', default=0)
    price = models.FloatField(verbose_name='报价', default=0)
    deal_money = models.FloatField('成交金额', default=0)
    transferee_peo = models.CharField('受让人', default='', max_length=16)
    licensor = models.CharField(verbose_name='出让方', max_length=64, default='')
    trading_conditions = models.CharField(verbose_name='交易条件', default='', max_length=200)
    plan_conditions = models.CharField(verbose_name='规划条件', default='', max_length=200)
    file_url = models.CharField('文件路径', null=True, blank=True, max_length=32)


# 楼市供应表
class BuildingSupplyF(models.Model):
    create_on = models.DateField('创建时间', auto_now_add=True)
    city = models.CharField('城市', max_length=16, default='')
    acreage = models.FloatField('面积', default=0)
    tao_num = models.IntegerField('套数', default=0)
    year_month = models.CharField('年月', default='', max_length=32)


# 楼市成交表
class BuildingSupplyT(models.Model):
    create_on = models.DateField('创建时间', auto_now_add=True)
    city = models.CharField('城市', max_length=16, default='')
    acreage = models.FloatField('面积', default=0)
    year_month = models.CharField('年月', default='', max_length=32)
    tao_num = models.IntegerField('套数', default=0)
    deal_average = models.FloatField('成交均价', default=0)


# 价值楼盘表
class ValueBuilding(models.Model):
    create_on = models.DateField('创建时间', auto_now_add=True)
    city = models.CharField('城市', max_length=16, default='')
    area = models.CharField('区', max_length=16, default='')
    project_name = models.CharField('项目名称', max_length=64, default='')
    location = models.CharField(verbose_name='位置', max_length=64, default='')
    total_building_area = models.FloatField('总建筑面积', default=0)
    land_area = models.FloatField(verbose_name='用地面积', default=0)
    plot_ratio = models.FloatField(verbose_name='容积率', default=0)
    total_tao = models.IntegerField('总套数', default=0)
    selling_tao = models.IntegerField('在售套数', default=0)
    yitui_tao = models.IntegerField('已推套数', default=0)
    in_average = models.FloatField('入市均价', default=0)
    selling_average = models.FloatField('在售均价', default=0)
    product_composition = models.CharField('产品构成', max_length=64, default='')
    h_area = models.CharField('户型和面积段', max_length=64, default='')
    supporting_business = models.CharField('商业配套', max_length=200, default='')
    supporting_education = models.CharField('教育配套', max_length=200, default='')
    traffic_conditions = models.CharField('交通状况', max_length=200, default='')
    developers = models.CharField('开发商', max_length=32, default='')
    sales = models.IntegerField('当月去化套数', default=0)
    first_time = models.CharField('首开日期', max_length=32, default='')


class Top_In(models.Model):
    create_on = models.DateField('创建时间', auto_now_add=True)
    city = models.CharField('城市', max_length=16, default='')
    in_time = models.CharField('首开日期', max_length=32, default='')
    company_name = models.CharField('企业名称', max_length=32, default='')
    develop_project = models.CharField('开发项目', max_length=32, default='')
    new_ranking = models.IntegerField('最新排名', default=0)
    headquarters_location = models.CharField('总部所在地', max_length=16, default='')


class BigData(models.Model):
    create_on = models.DateField('创建时间', auto_now_add=True)
    city = models.CharField('城市', max_length=16, default='')
    positioning = models.CharField('定位', max_length=32, default='')
    city_card = models.CharField('城市名片', max_length=256, default='')
    GDP = models.FloatField('GDP', default=0)
    peo_num = models.FloatField('人口', default=0)
    pillar_industries = models.CharField('支柱产业', max_length=256, default='')
    key_enterprises = models.CharField('重点企业', max_length=256, default='')
    development_plan = models.CharField('发展规划', max_length=256, default='')
    planning_for = models.TextField('规划利好', default='')
    file_url = models.CharField('文件路径', null=True, blank=True, max_length=32)


class Memo(models.Model):
    m_date = models.CharField('时间', max_length=64, default='')
    content = models.TextField('备忘录内容', default='')
    user_id = models.IntegerField('用户id', default=0)


# 收藏表
class Collection(models.Model):
    information_id = models.CharField('资讯id', max_length=64, default='')
    user_id = models.IntegerField('用户id', default=0)
    luyou = models.CharField('路由', default='', max_length=32)
    create_on = models.DateField('创建时间', auto_now_add=True)
    # universal_type = models.IntegerField('类型', default=0)


# 查看表
class ReceivePeo(models.Model):
    information_id = models.CharField('资讯id', max_length=64, default='')
    user_id = models.IntegerField('用户id', default=0)
    luyou = models.CharField('路由', default='', max_length=32)
    create_on = models.DateField('创建时间', auto_now_add=True)


# 邀请表
class YaoQing(models.Model):
    luyou = models.CharField('路由', default='', max_length=32)
    land_id = models.IntegerField('资讯id', default=0)
    user_id = models.IntegerField('用户id', default=0)
    yaoqingren = models.IntegerField('邀请人id', default=0)
    create_on = models.DateTimeField('创建时间', auto_now_add=True)


# 邀请已读表
class YaoQingRead(models.Model):
    yaoqing_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    create_on = models.DateTimeField(auto_now_add=True)


# 审核意见表
class AuditOpinion(models.Model):
    land_id = models.IntegerField('资讯id', default=0)
    opinion = models.CharField('审核意见', max_length=255, default='')
    source = models.CharField('来源', max_length=8, default='')
    user_id = models.IntegerField('发布者', default=0)
    create_on = models.DateField('创建时间', auto_now_add=True)



