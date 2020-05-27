from django.db import models


# Create your models here.
class Preview(models.Model):
    # 轮播图
    title = models.CharField(verbose_name='标题', max_length=200)


class SystemMessageModel(models.Model):
    content = models.CharField('消息内容', max_length=500, default='')
    create_on = models.DateTimeField('创建时间', auto_now_add=True)
    sys_type = models.CharField('类别', max_length=16, default='')
    user_id = models.IntegerField('用户id', default=0)
    trade_no = models.CharField('交易号', max_length=32,default='1')


class SystemRead(models.Model):
    user_id = models.IntegerField('用户id', default=0)
    sys_id = models.IntegerField('推送id', default=0)
    create_on = models.DateTimeField('创建时间', auto_now_add=True)


# 积分记录表
class IntegralRecord(models.Model):
    create_on = models.DateTimeField('创建时间', auto_now_add=True)
    integral_type = models.CharField('类别', default='', max_length=16)
    user_id = models.IntegerField('用户id', default=0)
    integral = models.IntegerField('获得的积分', default=0)


class LjyUser(models.Model):
    phone = models.CharField('手机号', default='', max_length=11)
    password = models.CharField('密码', default='', max_length=500)
    create_on = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    login_num = models.IntegerField(default=1, verbose_name="登陆次数")


# 挑刺功能----五个问题表
class Discern(models.Model):
    user_id = models.IntegerField('用户id', default=0)
    first_question = models.TextField('问题1', max_length=500, default='', null=True, blank=True)
    second_question = models.TextField('问题2', max_length=500, default='', null=True, blank=True)
    third_question = models.TextField('问题3', max_length=500, default='', null=True, blank=True)
    fourth_question = models.TextField('问题4', max_length=500, default='', null=True, blank=True)
    fifth_question = models.TextField('问题5', max_length=500, default='', null=True, blank=True)
    state = models.IntegerField('状态', default=0)
    fen = models.IntegerField('分', default=0)


# 一次性弹窗 TODO:
class NeiCe(models.Model):
    user_id = models.IntegerField('用户id', default=0)
    create_on = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    user_status = models.IntegerField('是否已看', default=0)
    leibie = models.CharField('类别', default='', max_length=16)


# 客服历史纪录
class HistoryRecord(models.Model):
    bond = models.CharField('纽带', default='', max_length=16)
    record = models.TextField('记录', default='')


# 用户列表
class UserListModel(models.Model):
    customer_id = models.IntegerField('客服id', default=0)
    y_list = models.TextField('广播列表', default='')