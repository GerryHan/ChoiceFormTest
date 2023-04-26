# -*- coding = utf-8 -*-
# @Time: 2023/3/19 11:02
# @Author: Gerry
# @File: login_demo.py
# @Software: PyCharm
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcsl_v1_5
from Crypto.PublicKey import RSA
import base64
import re
from requests import sessions

env = "dev"

if env == "test":
    # ************************** 测试环境协议域名 **************************
    protocol = "https"
    host = "test.isrm.going-link.com"
    port = ""
    secHost = ""

elif env == "prod":
    # ************************** 正式环境协议域名 **************************
    protocol = "https"
    host = "isrm.going-link.com"
    port = ""
    secHost = ""

else:
    # ************************** 开发环境协议域名 **************************
    protocol = "https"
    host = "dev.isrm.going-link.com"
    port = ""
    secHost = ""


def returnUrl(path):
    if not path.startswith("http"):
        return protocol + "://" + secHost + host + port + path
    else:
        return path


def encrypt(password):
    """
    明文密码RSA加密
    :param password:
    :return:
    """
    public_key = '''-----BEGIN PUBLIC KEY-----
    MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJL0JkqsUoK6kt3JyogsgqNp9VDGDp+t3ZAGMbVoMPdHNT2nfiIVh9ZMNHF7g2XiAa8O8AQWyh2PjMR0NiUSVQMCAwEAAQ==
    -----END PUBLIC KEY-----
    '''
    b_password = bytes(password, encoding="utf8")
    rsa_key = RSA.importKey(public_key)
    cipher = Cipher_pkcsl_v1_5.new(rsa_key)
    return base64.b64encode(cipher.encrypt(b_password)).decode()


def login(userName, password):
    """
    登录-
    :param userName:
    :param password:
    :return:
    """
    # 1.0登录(因为是dev环境解密,所以使用dev环境账号登录获取token)
    data = {"username": userName, "password": encrypt(password)}
    session = sessions.session()
    r_login = session.request(method="post", url=returnUrl("/oauth/"), data=data, allow_redirects=False)
    cookie = r_login.headers.get('Set-Cookie')
    redirect_url = r_login.headers.get('location')
    headers = {}
    if cookie is not None and 'type=account' not in redirect_url:
        authorization = session.request(method="get", url=returnUrl(f"/oauth/oauth/authorize?response_type=token&client_id=srm-portal&redirect_uri={redirect_url}/?hasLogin=true"), allow_redirects=False)
        access_token = "bearer " + re.search("access_token=(.*?)&", authorization.headers["location"]).group(1)
        headers = dict(Authorization=access_token)

    print(headers)


if __name__ == '__main__':
    login(userName="18011223344", password="hand1234")
