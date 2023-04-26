# -*- coding = utf-8 -*-
# @Time: 2023/2/1 16:05
# @Author: Gerry
# @File: rsaTool.py
# @Software: PyCharm
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcsl_v1_5
from Crypto.PublicKey import RSA
import base64


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