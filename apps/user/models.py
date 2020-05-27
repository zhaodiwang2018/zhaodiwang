from django.db import models


class Users(models.Model):
    """用户模型类"""
    DoesNotExist = None
    objects = None

    username = models.CharField(max_length=50, verbose_name="用户名")
    mobile = models.CharField(max_length=50, verbose_name='手机号')
    password = models.CharField(max_length=5000, blank=True, verbose_name='密码')
    create_on = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    token = models.CharField('头', max_length=300, null=True, blank=True)
    admin_token = models.CharField('后台头', max_length=300, null=True, blank=True)
    usertype = models.CharField(default='', verbose_name="用户类型", max_length=16)
    status = models.IntegerField(default=1, verbose_name='用户状态')
    city = models.CharField("湖北省内主管城市", max_length=40, default='[]')
    job = models.CharField(max_length=50, verbose_name='职位', null=True, blank=True)
    company = models.CharField(max_length=50, verbose_name='公司名称', null=True, blank=True)
    ranking_company = models.CharField(max_length=50, verbose_name='公司排名', default='无')
    addr = models.CharField(max_length=50, verbose_name='公司地址', null=True, blank=True)
    address_scale = models.CharField(default='', verbose_name="用地规模", max_length=16, null=True, blank=True)
    plot_ratio = models.CharField(default='', verbose_name="容积率", max_length=16, null=True, blank=True)
    invest_pattern = models.CharField(default='', verbose_name="投资模式", max_length=16, null=True, blank=True)
    land_nature = models.CharField(default='', verbose_name="用地性质", max_length=16, null=True, blank=True)
    area = models.CharField("区域", max_length=40, default='[]')
    intro = models.TextField(verbose_name='个人简介', null=True, blank=True)
    img = models.CharField('头像', default='1565251504.png', max_length=32)
    login_num = models.IntegerField(default=1, verbose_name="登陆次数")
    is_admin = models.SmallIntegerField(default=0, verbose_name='是否管理者')
    vip_num = models.IntegerField('vip', default=0)
    integration = models.IntegerField('积分', default=0)
    t_int = models.IntegerField('挑刺积分', default=0)
    y_int = models.IntegerField('邀请积分', default=0)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    user = models.ForeignKey(Users, verbose_name="用户", related_name='orders', on_delete=models.CASCADE, null=True)
    luyou = models.CharField('路由', max_length=32, default='')
    land_id = models.IntegerField('信息id', default=0)
    order_sn = models.CharField("订单号", max_length=50, null=True, blank=True)
    trade_no = models.CharField('交易号', max_length=100, null=True, blank=True)
    pay_status = models.CharField("订单状态", default="paying", max_length=30, )
    subject = models.CharField("标题", default="", max_length=100)
    order_mount = models.FloatField("订单金额", default=0.0)
    pay_time = models.DateTimeField("支付时间", auto_now_add=True)
    order_type = models.IntegerField('支付方式', default=1)  # 1:支付宝，2：微信，3：积分兑换，4：后台政府年会员开通，5：会员抵扣

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name


# 过期时间
class VipExpire(models.Model):
    expire_time = models.DateTimeField('到期时间')
    user_id = models.IntegerField('user', default=0)


# 发布记录
class ReleaseRecord(models.Model):
    user_id = models.IntegerField('发布用户id', default=0)
    land_id = models.IntegerField('发布信息id', default=0)
    luyou = models.CharField('路由', default='', max_length=32)
    create_on = models.DateTimeField('创建时间', auto_now_add=True)


# 被联系表
# class Contacted(models.Model):
#     land_id = models.CharField('id', max_length=64, default='')
#     user_id = models.IntegerField('用户id', default=0)
#     luyou = models.CharField('路由', default='', max_length=32)
#     create_on = models.DateField('创建时间', auto_now_add=True)


# 联系表
class Contact(models.Model):
    land_id = models.CharField('id', max_length=64, default='')
    user_id = models.IntegerField('联系者id', default=0)
    contacted_id = models.IntegerField('被联系者id', default=0)
    luyou = models.CharField('路由', default='', max_length=32)
    create_on = models.DateField('创建时间', auto_now_add=True)


# 赞表
class Zan(models.Model):
    land_id = models.CharField('id', max_length=64, default='')
    user_id = models.IntegerField('用户id', default=0)
    luyou = models.CharField('路由', default='', max_length=32)
    zc = models.IntegerField('赞或者踩', default=0)
    create_on = models.DateField('创建时间', auto_now_add=True)


# 充值条数表
class ChargeNumber(models.Model):
    user_id = models.IntegerField('用户id', default=0)
    nitui = models.IntegerField(default=0)
    paimai = models.IntegerField(default=0)
    zhuanrang = models.IntegerField(default=0)
    zhaoshang = models.IntegerField(default=0)
    xiancheng = models.IntegerField(default=0)
    shalong = models.IntegerField(default=0)
    yuebao = models.IntegerField(default=0)
    nadi = models.IntegerField(default=0)
    gongdi = models.IntegerField(default=0)
    shoufang = models.IntegerField(default=0)
    loupan = models.IntegerField(default=0)
    yuebaodata = models.IntegerField(default=0)
    zhoubao = models.IntegerField(default=0)
    jibao = models.IntegerField(default=0)


# 登录记录表
class LoginRecord(models.Model):
    user_id = models.IntegerField('id', default=0)
    create_on = models.DateField('日期', auto_now_add=True)


# 打卡记录表
class ClockRecord(models.Model):
    user_id = models.IntegerField('id', default=0)
    create_on = models.DateField('日期', auto_now_add=True)
    question = models.CharField('问题', max_length=500, default='')


# 邀请注册表
class InviteRegister(models.Model):
    invite_peo_id = models.IntegerField('邀请人id', default=0)
    register_peo_id = models.IntegerField('注册人id', default=0)
    yq_type = models.CharField('邀请注册或者邀请付费', max_length=8, default='')
    create_on = models.DateField('日期', auto_now_add=True)


# 日历
class Calendar(models.Model):
    c_date = models.CharField('时间', max_length=64, default='')
    big_list = models.TextField('大列表', default='')


class PaiMing(models.Model):
    user_id = models.IntegerField('id', default=0)
    username = models.CharField('名字', default='', max_length=64)
    act_num = models.FloatField('积分', default=0.0)


class Company(models.Model):
    username = models.CharField('名字', default='', max_length=64)
    register_num = models.FloatField('注册人数', default=0.0)


class Customer(models.Model):
    name = models.CharField(default='', max_length=8)
    phone = models.CharField(default='', max_length=16)


class AdminUserChart(models.Model):
    user_all = models.IntegerField('用户总数', default=0)
    new_user = models.IntegerField('今日新增用户数', default=0)
    today_chakan = models.IntegerField('今日查看数', default=0)
    today_shoucang = models.IntegerField('今日收藏数', default=0)
    today_fufei = models.IntegerField('今日付费数', default=0)
    create_on = models.DateField(auto_now_add=True)

