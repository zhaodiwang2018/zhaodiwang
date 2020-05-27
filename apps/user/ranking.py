# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 10:54
# @Author  : Liu
# @Email   : 15037822850@163.com
# @File    : ranking.py
# @Software: PyCharm
from rest_framework.views import APIView, Response
from apps.user.models import *
from apps.land.models import *
from apps.land.a import metric
from rest_framework import serializers
from apps.utils.mixin_utils import *
import operator
import datetime
import threading
import time
import pymysql

"""
活跃度排行榜
排名方式：
    活跃度 = 查看文章次数 * 50% + 收藏文章数 * 10% + 积分 * % 30 + 消费金额 * % 10
"""


class SelfRankingListViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = PaiMing
        fields = ('user_id', 'username', 'act_num')


class CompanyRankingListViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('username', 'register_num')


class RankingListView(LoginRequiredMixin, APIView):
    @metric
    def get(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        page = int(request.GET.get('page'))
        ranking_info = PaiMing.objects.order_by('-act_num')
        rank_list = []
        for rank in ranking_info:
            rank_dict = {'user_id':rank.user_id, 'username': rank.username, 'act_num': rank.act_num}
            rank_list.append(rank_dict)
        user_self = PaiMing.objects.filter(user_id=user.id).first()
        if not user_self:
            return Response({'data': rank_list[(page - 1) * 20:(page - 1) * 20 + 20], 'msg': '获取成功', 'status': '1'})
        return Response({'data': rank_list[(page - 1) * 20:(page - 1) * 20 + 20], 'user_rank': int(rank_list.index({'user_id':user.id, 'username': user.username, 'act_num': user_self.act_num})) + 1, 'user_act_num': user_self.act_num, 'msg': '获取成功', 'status': '1'})

    def post(self, request):
        user = Users.objects.filter(mobile=get_user_id(request)).first()
        page = int(request.data.get('page'))
        ranking_info = Company.objects.order_by('-register_num')
        rank_list = []
        for rank in ranking_info:
            rank_dict = {'username': rank.username, 'register_num': rank.register_num}
            rank_list.append(rank_dict)
        user_self = Company.objects.filter(username=user.ranking_company).first()
        print(user_self)
        if not user_self:
            return Response({'data': rank_list[(page - 1) * 20:(page - 1) * 20 + 20], 'msg': '获取成功', 'status': '1'})
        return Response({'data': rank_list[(page - 1) * 20:(page - 1) * 20 + 20], 'user_rank': int(rank_list.index({'username': user.ranking_company, 'register_num': user_self.register_num})) + 1, 'user_act_num': user_self.register_num, 'company': user_self.username, 'msg': '获取成功', 'status': '1'})


# def Delete_From(company_self):
#     # 打开数据库链接
#     db = pymysql.connect("118.31.60.22", "root", "admin123", "zhaodi")
#
#     # 使用cursor()方法获取操作游标
#     cursor = db.cursor()
#     if company_self == 'self_ranking':
#         # SQL语句更新数据
#         sql = """TRUNCATE TABLE user_paiming"""
#
#         try:
#             # 执行SQL语句
#             cursor.execute(sql)
#             # 提交到数据库执行
#             db.commit()
#             print("删除个人数据成功")
#
#         except Exception as e:
#             print("删除数据失败：case%s" % e)
#             # 发生错误时回滚
#             db.rollback()
#
#         finally:
#             # 关闭游标连接
#             cursor.close()
#             # 关闭数据库连接
#             db.close()
#     elif company_self == 'company_ranking':
#         # SQL语句更新数据
#         sql = """TRUNCATE TABLE user_company"""
#
#         try:
#             # 执行SQL语句
#             cursor.execute(sql)
#             # 提交到数据库执行
#             db.commit()
#             print("删除公司数据成功")
#
#         except Exception as e:
#             print("删除数据失败：case%s" % e)
#             # 发生错误时回滚
#             db.rollback()
#
#         finally:
#             # 关闭游标连接
#             cursor.close()
#             # 关闭数据库连接
#             db.close()
#
# @metric
# def self_func():
#     company_self = 'self_ranking'
#     Delete_From(company_self)
#     users = Users.objects.filter(is_admin=0, usertype='1')
#     active_list = []
#     for user in users:
#         if user.username.isdigit() is False:
#             colection_num = Collection.objects.filter(user_id=user.id).count()
#             orders = OrderInfo.objects.filter(user_id=user.id, pay_status='TRADE_SUCCESS', order_type__in=[1, 2])
#             money = 0
#             if orders:
#                 for order in orders:
#                     money += order.order_mount
#             active_num = user.login_num * 0.5 + colection_num * 0.1 + user.integration * 0.3 + money * 0.1
#             info = {'user_id': user.id, 'username': user.username, 'active_num': round(active_num, 2)}
#             active_list.append(info)
#     data_list = sorted(active_list, key=operator.itemgetter('active_num'), reverse=True)
#     for data in data_list:
#         PaiMing.objects.create(username=data['username'], act_num=data['active_num'], user_id=data['user_id'])
#     # 如果需要循环调用，就要添加以下方法
#     print('30')
#     company_s = 'company_ranking'
#     Delete_From(company_s)
#     print('cha')
#     company_list = []
#     for user in users:
#         if user.ranking_company or user.ranking_company != '无':
#             if len(user.ranking_company) > 1:
#                 company_list.append(user.ranking_company)
#     num_company = []
#     for u_s in users:
#         if u_s.ranking_company:
#             if len(u_s.ranking_company) > 1:
#                 n_m = {'company': u_s.ranking_company, 'num': company_list.count(u_s.ranking_company)}
#                 num_company.append(n_m)
#     ignored_keys = ["num"]
#     filtered = {tuple((k, d[k]) for k in sorted(d) if k not in ignored_keys): d for d in num_company}
#     dst_lst = list(filtered.values())
#     data_lists = sorted(dst_lst, key=operator.itemgetter('num'), reverse=True)
#     for datas in data_lists:
#         Company.objects.create(username=datas['company'], register_num=datas['num'])
    # 如果需要循环调用，就要添加以下方法
    # timer = threading.Timer(86400, self_func)
    # print(111111111111111111)
    # timer.start()
# timer_self = threading.Timer(3, self_func)
# timer_self.start()





# @metric
# def company_ranking():
#     company_self = 'company_ranking'
#     Delete_From(company_self)
#     time.sleep(5)
#     users = Users.objects.filter(is_admin=0, usertype='1')
#     company_list = []
#     for user in users:
#         if user.company:
#             if len(user.company) > 1:
#                 company_list.append(user.company)
#     num_company = []
#     for u_s in users:
#         if u_s.company:
#             if len(u_s.company) > 1:
#                 n_m = {'company': u_s.company, 'num': company_list.count(u_s.company)}
#                 num_company.append(n_m)
#     ignored_keys = ["num"]
#     filtered = {tuple((k, d[k]) for k in sorted(d) if k not in ignored_keys): d for d in num_company}
#     dst_lst = list(filtered.values())
#     data_list = sorted(dst_lst, key=operator.itemgetter('num'), reverse=True)
#     n = 1
#     for data in data_list:
#         Company.objects.create(rank=n, username=data['company'], register_num=data['num'])
#         n += 1
#     # 如果需要循环调用，就要添加以下方法
#     timers = threading.Timer(86400, company_ranking)
#     timers.start()
#     print('插入成功')

# 获取现在时间
# now_time = datetime.datetime.now()
# # 获取明天时间
# next_time = now_time + datetime.timedelta(days=+1)
# next_year = next_time.date().year
# next_month = next_time.date().month
# next_day = next_time.date().day
# # 获取明天3点时间
# next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 03:00:00",
#                                        "%Y-%m-%d %H:%M:%S")
# # 获取距离明天3点时间，单位为秒
# timer_start_time = (next_time - now_time).total_seconds()
# print("%s秒后重新排名" % timer_start_time)
# 定时器,参数为(多少时间后执行，单位为秒，执行的方法)

# print('休眠20秒')
# time.sleep(20)

# now_time_company = datetime.datetime.now()
# next_time_company = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 04:00:00",
#                                        "%Y-%m-%d %H:%M:%S")
# # 获取距离明天3点时间，单位为秒
# timer_start_time_company = (next_time_company - now_time_company).total_seconds()
# print("%s秒后公司重新排名" % timer_start_time_company)
#
# timer_company = threading.Timer(30, company_ranking)
# timer_company.start()
"""
【找地网】尊敬的***用户，感谢您对找地网的支持和信任，系统检测到您的资料不完整或不规范，为能够提供更加精准信息，希望您尽早完善。
"""
