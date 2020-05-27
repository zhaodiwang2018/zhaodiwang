# # -*- coding: utf-8 -*-
# # @Time    : 2019/8/28 17:04
# # @Author  : Liu
# # @Email   : 15037822850@163.com
# # @File    : a.py
# # @Software: PyCharm
# import os
import time
import datetime, pytz

# print(datetime.datetime.now().month)
# print(datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')))

# import time
# a = time.time()
# print(int(a * 100000))
# #
# # f = "[{'status': 'success', 'uid': 1567472802720, 'url': '156747354881.jpg'}, {'status': 'success', 'uid': 1567472806451, 'url': '156747354871.jpg'}, {'status': 'success', 'uid': 1567472811494, 'url': '156747354823.jpg'}, {'status': 'success', 'uid': 1567472815577, 'url': '156747354822.jpg'}]"
# #
# # print(len(f))
#
# # for i in range(len(f)):
# #     filedate = os.path.getmtime(‘G:\\qtp\\‘ + f[i])
# #     time1 = datetime.datetime.fromtimestamp(filedate).strftime(‘ % Y - % m - % d‘)
# #     date1 = time.time()
# #     num1 = (date1 - filedate) / 60 / 60 / 24
# #     if num1 >= 30:
# #         os.remove(‘G:\\qtp\\‘ + f[i])
# #         print("已删除文件：%s ： %s" % (time1, f[i]))
# #         else:
# #         print("there are no file more than 30 days")
# # import ssh
# # client=ssh.SSHClient()
# # client.set_missing_host_key_policy(ssh.AutoAddPolicy())
# # client.connect("ip地址",port=22,username="用肪名",password="密码")
# # stdin,stdout,stderr=client.exec_command("ls/目录")
# # print stdout.read()
# # print(type(time.time()))
# # unit = 3600*24
# # start_time = int(time.time()) / unit * unit - 8 * 3600
# # print(start_time)
# #
# # print(111111111111)
# c =datetime.datetime.now()
# cur_date_first = datetime.datetime(datetime.date.today().year, datetime.date.today().month, 1)
# cur_date_last = datetime.datetime(datetime.date.today().year, datetime.date.today().month + 1, 1) - datetime.timedelta(
#     1)
# a = time.mktime(cur_date_first.timetuple())
# b = time.mktime(cur_date_last.timetuple())
# if b<c<a:
#
# print(cur_date_last)
# print(cur_date_first,cur_date_last)
# # a = 2
# # if 1 < a < 5:
# #     print(111)
#
#
# import re
# password = '2daaa2233{'
# ret = re.match(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z_\.\s]{8,18}$', password)
# print(ret)
# import time
# # cur_date_first = datetime.datetime(datetime.date.today().year, 1,1)
# # cur_date_last = datetime.datetime(datetime.date.today().year, 12,31)
# # c = datetime.date.today()
# # a = time.mktime(c.timetuple())
# # d = time.mktime(cur_date_last.timetuple())
#
# # print(a, d)
# # print(cur_date_first, cur_date_last)
# d = datetime.datetime.now()
# dayscount = datetime.timedelta(days=d.isoweekday())
# dayto = d - dayscount
# sixdays = datetime.timedelta(days=6)
# dayfrom = dayto + sixdays
# date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
# date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
# # print()
# # s = time.mktime(dayfrom.timetuple())
# # print(s)
# # date_from = datetime.datetime(s.year, s.month, s.day, 0, 0, 0)
# # date_to = datetime.datetime(s.year, s.month, s.day, 23, 59, 59)
# print(date_from, date_to)

# a = {'a':1, 'b':2, 'c':3}
import pytz

# print(datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')))
# sixdays = datetime.timedelta(days=6)
# today = datetime.date.today()
# print(today)
# dayscount = datetime.timedelta(days=today.isoweekday())
# print(dayscount)
# print(sixdays)
# threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 3))
# print(threeDayAgo)
# 列表转成字符串

import time, functools


def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        time0 = time.time()
        ret = fn(*args, **kw)
        time1 = time.time()
        print('%s executed in %s ms' % (fn.__name__, time1 - time0))
        return ret

    return wrapper


# def use_logging(level):
#     def _deco(func):
#         def __deco(*args, **kwargs):
#             if level == "warn":
#                 print("%s is running" % func.__name__)
#             return func(*args, **kwargs)
#
#         return __deco
#
#     return _deco
#
#
# @use_logging(level="warn")
# def login():
#     print('logging')
# login()
# 等价于use_logging(level="warn")(bar)(1,3)

# d = {}
# for x in L:
#     d[x] = 1
# mylist = list(d.keys())
# print(d)
# print(mylist)
# listx = [1,2,3,4,5,6,7]       # 7 个元素
# listy = [2,3]         # 6 个元素
# listz = [100,100,100,100]     # 4 个元素
# list_result = map(lambda x,y,z : x**2 + y + z,listx, listy, listz)
# print(list(list_result))

# today = datetime.date.today()
# today_timeArray = time.strptime(str(today)[:10], "%Y-%m-%d")
# # print(today_timeArray)
# # 今天的时间戳
# today_time = time.mktime(today_timeArray)
# # print(today_time)
# a = '2019-11-01'
# timeArray = time.strptime(a, "%Y-%m-%d")
# # print(timeArray)
# timestamp = time.mktime(timeArray)
# # print(timestamp)
# a = 20
# b = 30
# c = 40
# d = 50
# active_num = a * 0.5 + b * 0.1
# # print(active_num)
# from pandas import Series
# import pandas as pd
#
# obj = pd.Series([7, -5, 7, 4, 2, 0, 4])
# print(obj.rank())

import threading

# def fun_timer():
#     print('Hello Timer!')
#     global timer
#     timer = threading.Timer(3, fun_timer)
#     timer.start()
#
#
# timer = threading.Timer(1, fun_timer)
#
# timer.start()


# def doSth():
#     print('test')
#     # 假装做这件事情需要一分钟
#     time.sleep(60)
#
#
# def main(h=0, m=0):
#     '''h表示设定的小时，m为设定的分钟'''
#     while True:
#         # 判断是否达到设定时间，例如0:00
#         while True:
#             now = datetime.datetime.now()
#             # 到达设定时间，结束内循环
#             if now.hour == h and now.minute == m:
#                 break
#             # 不到时间就等20秒之后再次检测
#             time.sleep(20)
#             doSth()
#
#
# main(15, 34)

import datetime
import threading
import requests
# def func():
#     s = requests.get(url).json()
#
#     #如果需要循环调用，就要添加以下方法
#     timer = threading.Timer(86400, func)
#     timer.start()
#
# # 获取现在时间
# now_time = datetime.datetime.now()
# # 获取明天时间
# next_time = now_time + datetime.timedelta(days=+1)
# next_year = next_time.date().year
# next_month = next_time.date().month
# next_day = next_time.date().day
# # 获取明天3点时间
# next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 03:00:00", "%Y-%m-%d %H:%M:%S")
# # # 获取昨天时间
# # last_time = now_time + datetime.timedelta(days=-1)
#
# # 获取距离明天3点时间，单位为秒
# timer_start_time = (next_time - now_time).total_seconds()
# print(timer_start_time)
# # 54186.75975
#
#
# #定时器,参数为(多少时间后执行，单位为秒，执行的方法)
# timer = threading.Timer(timer_start_time, func)
# timer.start()
# b = 1
# a = {}
# a[b] = {'a':2}
# print(a)