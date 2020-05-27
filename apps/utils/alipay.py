# -*- coding: utf-8 -*-

# pip install pycryptodome
__author__ = 'bobby'

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes
from zhaodi.settings import ali_pub_key_path, private_key_path, ALI_APP_ID


import json


class AliPay(object):
    """
    支付宝支付接口
    """
    def __init__(self, app_id, notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.app_id = app_id
        self.notify_url = notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.import_key(fp.read())


        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.app_id,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        # ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    return_url = 'https://openapi.alipaydev.com/gateway.do?app_id=2016100100643128&biz_content=%7B%22subject%22%3A%22%5Cu6d4b%5Cu8bd5%5Cu8ba2%5Cu53552%22%2C%22out_trade_no%22%3A%2220170202988%22%2C%22total_amount%22%3A100%2C%22product_code%22%3A%22FAST_INSTANT_TRADE_PAY%22%7D&charset=utf-8&method=alipay.trade.page.pay&notify_url=http%3A%2F%2F118.31.60.22%3A8000%2Fuser%2Fali_pay%2F&return_url=http%3A%2F%2F118.31.60.22%3A8000%2Fuser%2Fali_pay%2F&sign_type=RSA2&timestamp=2019-09-09+16%3A49%3A54&version=1.0&sign=ZugUUqvbLSxcdP%2F46NtvkrTfVKaOmQQsmIhsMhG6FGkRXHH9mgRNpprhp5bs%2BQ4jpOE1AEejz2XukqOX5Ca94Ssx3sAMtZaoGsrrgzBLgsyWxK4vX9yUX2qgtiXVSIVzzFFsb5m6wTUEHjRtror03Ci%2Fm7NABsrineOpYe40E5SvgUksmePGpG5B4jcoenntYkEGnplwKPuMF6YoRqaxboR4n08ik1ieVTxeVsXfNZLkXe0ccO7NXgSY%2BRV7JIKCGDkAHZDBE6IRUenFmGjFCTfIRvmS3xaENKHOSGRk3UMEwQeAn31b8xqG80jXeKshblcFDAtelau1d%2FD%2BEmgXDg%3D%3D'
    o = urlparse(return_url)
    query = parse_qs(o.query)
    processed_query = {}
    ali_sign = query.pop("sign")[0]


    alipay = AliPay(
        app_id=ALI_APP_ID,
        notify_url="http://118.31.60.22:8000/user/ali_pay/",
        app_private_key_path=private_key_path,
        alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False,
        return_url="http://118.31.60.22:8000/user/ali_pay/"
    )

    for key, value in query.items():
        processed_query[key] = value[0]
    print(alipay.verify(processed_query, ali_sign))

    # url = alipay.direct_pay(
    #     subject="测试订单2",
    #     out_trade_no="20170202988",
    #     total_amount=100,
    #     return_url="http://118.31.60.22:8000/user/ali_pay/"
    # )
    # re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    #
    # print(re_url)
