# -*- coding = utf-8 -*-
# @Time: 2023/11/30 16:36
# @Author: Gerry
# @File: login2.py
# @Software: PyCharm
import datetime
import json
import random

from config.globals.userInfo import UserInfo
from tools import request
user = UserInfo()


def login(username, password, scene="testing@choiceform.com"):
    # 登录主接口,输入登录参数
    url = f"https://portal.choiceform.io/api/signin"
    data = {"email": username,
            "password": password}
    loginDic = request.post(url=url, json=data, parseToJson=False)
    assert loginDic.status_code == 201, "登陆失败的哇"
    loginDic1 = loginDic.text
    loginDic2 = json.loads(loginDic1)
    token = loginDic2.get("data").get("accessToken")
    assert token is not None, "access_token 为空"
    headers = dict(authorization="Bearer" + " " + token)
    print(headers)
    # 保存token
    UserInfo.setAccToken(scene=scene, token=headers, password=password)
    return headers


def sms_getNode(scene):
    """
    获取节点列表
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/sms_credentials?workspace_id=6385b14174a84547035e28ba"
    response = request.get(url=url, scene=scene, parseToJson=False)
    return response


def smsCreate(data, scene):
    """
    创建邮件
    :param data:
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/sms_credentials"
    response = request.post(url=url, json=data, scene=scene, parseToJson=False)
    return response


def smsDelete(scene):
    """
    删除邮件
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/sms_credentials/d2fc2a52-c8eb-44a8-a38f-fe01f885f7cd"
    response = request.delete(url=url, scene=scene, parseToJson=False)
    return response


def smsGet(scene):
    """
    获取邮件配置
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/sms_credentials/d2fc2a52-c8eb-44a8-a38f-fe01f885f7cd"
    response = request.get(url=url, scene=scene, parseToJson=False)
    return response


def smsUpdate(data, scene):
    """
    获取邮件配置
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/sms_credentials/d2fc2a52-c8eb-44a8-a38f-fe01f885f7cd"
    response = request.patch(url=url, json=data, scene=scene, parseToJson=False)
    return response


def smsUpdateA(data, scene):
    """
    更新邮件配置
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/sms_credentials/d2fc2a52-c8eb-44a8-a38f-fe01f885f7cd"
    response = request.put(url=url, json=data, scene=scene, parseToJson=False)
    return response


if __name__ == '__main__':
    login = login(username="testing@choiceform.com", password="cftesting")
    # 获取节点
    # sms_getNodeRes = sms_getNode(scene="testing@choiceform.com")
    # 创建邮件
    data = {
        "id": "d2fc2a52-c8eb-44a8-a38f-fe01f885f7cd",
        "name": "创建邮件服务的配置",
        "settings": {
            "key_id": "6385b14174a84547035e28ba",
            "key_secret": "key_secret",
            "provider": "aliyun"
        },
        "workspace_id": "6385b14174a84547035e28ba"
    }
    # smsCreateRes = smsCreate(data=data, scene="testing@choiceform.com")
    # 删除邮件
    smsDeleteRes = smsDelete(scene="testing@choiceform.com")

    # # 获取邮件服务配置
    # smsGetRes = smsGet(scene="testing@choiceform.com")

    # 更新邮件配置
    dataA = {
        "name": "更新邮件服务的配置",
        "settings": {
            "key_id": "key_id",
            "key_secret": "key_secret",
            "provider": "aliyun"
        }
    }
    # smsUpdateARes = smsUpdate(data=dataA, scene="testing@choiceform.com")


