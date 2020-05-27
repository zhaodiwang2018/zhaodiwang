import hashlib, time
import time
from django.core import signing
import hashlib
from django.core.cache import cache
import os, json


# 获取请求头里的token信息


def get_token(name):
    '''
    将当前时间戳转化为被hash的md5字符串
        - 注意：md5.update(内部必须插入bytes格式)
    :param name:
    :return:
    '''
    md5 = hashlib.md5()
    md5.update(str(time.time()).encode('utf-8'))
    md5.update(name.encode('utf-8'))
    return md5.hexdigest()


HEADER = {'type': 'JWP', 'alg': 'default'}
KEY = 'CHEN_FENG_YAO'
SALT = 'zhaodi.net.cn'
TIME_OUT = 24 * 60 * 60  # 24H


class UserToken():
    def encrypt(self, obj):
        """加密"""
        value = signing.dumps(obj, key=KEY, salt=SALT)
        value = signing.b64_encode(value.encode()).decode()
        return value

    def decrypt(self, src):
        """解密"""
        src = signing.b64_decode(src.encode()).decode()
        raw = signing.loads(src, key=KEY, salt=SALT)
        return raw

    def create_token(self, username):
        """生成token信息"""
        # 1. 加密头信息
        header = self.encrypt(HEADER)
        # 2. 构造Payload
        payload = {"username": username, "iat": time.time()}
        payload = self.encrypt(payload)
        # 3. 生成签名
        md5 = hashlib.md5()
        md5.update(("%s.%s" % (header, payload)).encode())
        signature = md5.hexdigest()
        token = "%s.%s.%s" % (header, payload, signature)
        # 存储到缓存中
        if username[11:] == 'phone':
            cache.set(username, token, 30 * 24 * 60 * 60)
        else:

            cache.set(username, token, TIME_OUT)
        return token

    def get_payload(self, token):
        if not token:
            return None
        payload = str(token).split('.')[1]
        payload = self.decrypt(payload)
        return payload

    # 通过token获取用户名
    def get_username(self, token):
        if not token:
            return None
        payload = self.get_payload(token)
        # a = payload['iat']
        # b = time.time()
        # c = b - a
        # print(a,b)
        # print(int(c))
        # print(payload['username'])
        return payload['username']

    def check_token(self, token):
        username = self.get_username(token)
        last_token = cache.get(username)
        if last_token:
            return last_token == token
        return False
