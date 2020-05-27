# # -*- coding: utf-8 -*-
# # @Time    : 2019/9/11 10:10
# # @Author  : Liu
# # @Email   : 15037822850@163.com
# # @File    : a.py
# # @Software: PyCharm
#
# import threading
# from dwebsocket.decorators import accept_websocket
#
# # 存储连接websocket的用户
# clients = {}
# # 记录连接人数   其实没什么卵用  = =
# count = 0
#
#
# # 连接websocket  ws://localhost：8000/websocketLink/22
# # 因为 websocket 是协议  所以不能用 http或https
# @accept_websocket
# def websocketLink(request, username):
#     '连接websocket'
#     global count
#     # 获取连接
#     if request.is_websocket:
#         lock = threading.RLock()  # rlock线程锁
#         try:
#             lock.acquire()  # 抢占资源
#             s = {}
#             #  因为同一个账号打开多个页面连接信息是不同的
#             if clients.get(username) != None:
#                 # 连接信息  键 连接名  值：连接保存
#                 s[str(request.websocket)] = request.websocket
#                 # 已存在的连接信息继续增加
#                 clients[username].update(s)
#             else:
#                 # 人数加1
#                 count = count + 1
#                 #  连接信息  键 连接名  值：连接保存
#                 s[str(request.websocket)] = request.websocket
#                 # 新增 用户  连接信息
#                 clients[username] = s
#             print("用户人数" + str(count))
#             print(request.websocket)
#             # 监听接收客户端发送的消息 或者 客户端断开连接
#             for message in request.websocket:
#                 if not message:
#                     break
#                 else:
#                     request.websocket.send(message)
#         finally:
#             # 通过用户名找到 连接信息 再通过 连接信息 k 找到 v (k就是连接信息)
#             clients.get(username).pop(str(request.websocket))
#             # 释放锁
#             lock.release()
#
#
# # 发送消息
# def websocketMsg(client, msg):
#     import json
#     # 因为一个账号会有多个页面打开 所以连接信息需要遍历
#     for cli in client:
#         'client客户端 ，msg消息'
#         b1 = json.dumps(msg).encode('utf-8')
#         client[cli].send(b1)
#
#
# # 服务端发送消息
# def send(username, title, data, url):
#     'username:用户名 title：消息标题 data：消息内容，消息内容:ulr'
#     try:
#         if clients[username]:
#             websocketMsg(clients[username], {'title': title, 'data': data, 'url': url})
#             # 根据业务需求 可有可无    数据做 持久化
#             # messageLog = MessageLog(name=username, msg_title=title, msg=data, msg_url=url, is_required=0)
#
#             flg = 1
#         flg = -1
#     except BaseException:
#         # messageLog = MessageLog(name=username, msg_title=title, msg=data, msg_url=url, is_required=1)
#         pass
#     finally:
#         pass


# a = 'code=0215ZULk1YLgoo0niLNk1MJNLk15ZULY&state=123'
# r = a.split('&')[0].split('=')[1]
# print(r)
#
# a_list = [{'武汉': [{'land_type': 2, 'title': '我是武汉1', 'land_id': 20, 'serial_number': '123456', 'img': '157190850579.png'},{'land_type': 1, 'title': '我是武汉2', 'land_id': 23, 'serial_number': '654123', 'img': '157190850579.png'}]},{'黄陂': [{'land_type': 1, 'title': '我是黄陂', 'land_id': 30, 'serial_number': '789654', 'img': '157190850579.png'}]},]
# spam = {'A':123 ,'B':345,'C':345 }
# for k,v in spam.items():
#     print(k,v)

# for k, v in b_list.items():
#     for s in v:
#         print(s)
#         if s['land_type'] == 2:
#             land_two += 1
#         else:
#             land_one += 1

# import time
#
# dt = "2016-05-05 20:28:54"
#
# # 转换成时间数组
# timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
# # 转换成时间戳
# timestamp = time.mktime(timeArray)
#
# print(timestamp)
# a = '1571760000'
# print(int(a))
import datetime
import math

#
# lists = [{'武汉': [{'land_id': 20},{'land_id': 23}]},{'黄陂': [{'land_id': 30}]}]
# # date_day = Calendar.objects.filter(c_date=land.advance_date).first()
# # if date_day:
# land_city = '武汉'
# land_id = 45
# s_list = []
# land_id_list = []
# for city_s in lists:
#     for c, o in city_s.items():
#         s_list.append(c)
#         for s in o:
#             land_id_list.append(s['land_id'])
# # print(land_id_list)
# # print(s_list)
# if land_id not in land_id_list:
#     flag = False
#     for s_l in s_list:
#         if land_city in s_l:
#             # print(land_city)
#             for ci_i in lists:
#                 # print(ci_i)
#                 l_list = ci_i.get(land_city)
#                 # print(l_list)
#                 if l_list:
#                     # print(l_list)
#                     l_list.append({'land_id': land_id})
#             flag = True
#     if flag is False:
#         # print(land_city)
#         info_list = []
#         info_obj = {'land_id': land_id}
#         info_list.append(info_obj)
#         info_dic = {land_city: info_list}
#         # print(info_dic)
#         lists.append(info_dic)

# print(lists)
# import xlrd
#
# book = xlrd.open_workbook('data.xlsx')
# sheet1 = book.sheets()[0]
# col3_values = sheet1.col_values(2)
# # print('第3列值',col3_values)
# x = []
# for va in col3_values:
#     if va != '手机号':
#         x.append(str(int(va)))
# print(len(x))
# mobiles = ','.join(str(n) for n in x)
# print(type(mobiles))
# import datetime, time
# import pytz
# today_datetime = datetime.datetime.now()
# print(today_datetime)
# today_datetime_str = \
#     today_datetime.strftime('%Y-%m-%d')
# today_datetime_datetime = datetime.datetime.strptime(today_datetime_str, '%Y-%m-%d')
# print(today_datetime_datetime)
# today = datetime.date.today()
# yesterday = today - datetime.timedelta(days=1)
# print(yesterday - a)
# today_timeArray = time.strptime(str(yesterday)[:10], "%Y-%m-%d")
# today_time = time.mktime(today_timeArray)
# print(today_time)
# now_time = int(time.mktime(now.timetuple()))
# print(today_time - now_time)
# r = 9
# a = [{'a': 1, 'b': 2},{'a': 3, 'b': 4},{'a': 5, 'b': 6}]
# result = filter(lambda x: x['a'] == r, a)
# if len(list(result)) == 0:
#     print(111)
# print(result)
