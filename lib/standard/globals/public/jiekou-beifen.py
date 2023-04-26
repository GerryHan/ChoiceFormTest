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


def generate_mobile():
    """随机生成一个手机号码。。    1[3,5,8,9] + 9"""
    phone = '1' + random.choice(["3", "5", "7", "8", "9"])
    for i in range(9):
        num = random.randint(1, 9)
        phone += str(num)
    return phone


def gender():
    """随机取一个性别。。"""
    gender_random = random.choice(["optY4Rapslr5z8CZvpi", "optY4Rapslr5z8CZvph"])
    return gender_random


def get_name():
    surname = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨", "朱",
               "何", "吕", "施", "张", "孔", "曹", "魏", "陶", "姜", "戚", "谢", "邹", "喻", "柏", "韦", "昌", "马",
               "凤", "花", "方", "俞", "任", "哪", "鲍", "史", "唐", "费", "廉", "岑", "薛", "雷", "乐", "于", "时",
               "皮", "姚", "邵", "堪", "汪", "祁", "毛", "禹", "狄", "米", "贝", "明", "臧", "计", "伏", "成", "戴",
               "熊", "纪", "舒", "屈", "项", "祝", "董", "梁", "秦", "宋", "傅", "苗", ]

    name = ["是", "我", "不", "人", "在", "他", "有", "这", "个", "上", "们", "来", "到", "时", "大", "为", "子", "中",
            "你", "说", "生", "国", "年", "着", "就", "那", "和", "要", "以", "会", "家", "可", "下", "而", "过", "天",
            "去", "能", "对", "好", "看", "起", "如", "事", "把", "还", "用", "第", "样", "道", "想", "作", "美", "总",
            "从", "无", "情", "面", "最", "女", "但", "现", "前", "动", "经", "长", "儿", "回", "位", "分", "老", "知",
            "世", "什", "两", "次", "使", "身", "者", "被", "高", "则", "房", "早", "院", "量", "苦", "火", "布", "品",
            "近", "坐", "产", "答", "星", "精", "视", "五", "巴", "奇", "管", "类", "未", "朋", "且", "婚", "台", "夜",
            "青", "北", "队", "久", "乎", "越", "观", "落"]
    Name = random.choice(surname)+random.choice(name)
    return Name


def Label():
    data_labelList = []
    for i in range(random.choice([1, 2, 3, 4])):
        data_label = random.choice([{
                "id": "optY4Ra-slr5z8CmZpZ",
                "color": "#A3A3A3",
                "name": "高消费"
            },
            {
                "id": "optY4Ra-slr5z8CmZpa",
                "color": "#A3A3A3",
                "name": "低消费"
            },
            {
                "id": "optY4Ra-slr5z8CmZpb",
                "color": "#A3A3A3",
                "name": "多次复购"
            },
            {
                "id": "optY4Ra-slr5z8CmZpc",
                "color": "#A3A3A3",
                "name": "未复购"
            }])
        data_labelList.append(data_label)
    return data_labelList


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


def query_Mdtable(scene):
    # 查询客户记录
    url = f"https://txapi.choiceform.io/api/v1/records?page=1&page_size=1000"
    data = {"datasheet_id": "dtsY4RcK8lr5z8Cmq8q",
            "keyword": ""}
    data_dict = request.post(url=url, json=data, scene=scene)
    return data_dict


def query_Buy(scene):
    # 购买记录接口
    url = f"https://txapi.choiceform.io/api/v1/records?page=1&page_size=1000"
    data = {"datasheet_id": "dtsY4Rbislr5z8Cq3mZ",
            "keyword": ""}
    data_dict = request.post(url=url, json=data, scene=scene)
    return data_dict


def webhook():
    # webhook接口
    url = f"https://txapi.choiceform.io/wf/v1/webhook/15d571ba-9300-4522-bf0c-56ff4fd6f128"
    data = {"data": 123,
            "number": 456}
    res = request.post(url=url, json=data, parseToJson=False)
    assert res.status_code == 204, "请求失败"
    return res


def create_Client(data, scene):
    """
    :param data:
    :param scene:
    :return:
    """
    # 创建数据表
    url = f"https://txapi.choiceform.io/api/v1/datasheets/dtsY4RaWclr5z8CtB-D/records"
    data_dict = request.post(url=url, json=data, scene=scene)
    return data_dict


def mail_getNode(scene):
    """
    获取节点列表
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/mail_credentials?workspace_id=6385b14174a84547035e28ba"
    response = request.get(url=url, scene=scene, parseToJson=False)
    return response


def mailCreate(data, scene):
    """
    创建邮件
    :param data:
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/mail_credentials"
    response = request.post(url=url, json=data, scene=scene, parseToJson=False)
    return response


def mailDelete(scene):
    """
    删除邮件
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/mail_credentials/9b5071ab-a37a-4a29-832e-b43cd3b7e4e6"
    response = request.delete(url=url, scene=scene, parseToJson=False)
    return response


def mailGet(scene):
    """
    获取邮件配置
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/mail_credentials/9b5071ab-a37a-4a29-832e-b43cd3b7e4e6"
    response = request.get(url=url, scene=scene, parseToJson=False)
    return response


def mailUpdate(data, scene):
    """
    获取邮件配置
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/mail_credentials/9b5071ab-a37a-4a29-832e-b43cd3b7e4e6"
    response = request.patch(url=url, json=data, scene=scene, parseToJson=False)
    return response


def mailUpdateA(data, scene):
    """
    获取邮件配置
    :param scene:
    :return:
    """
    url = f"https://txapi.choiceform.io/wf/api/v1/mail_credentials/9b5071ab-a37a-4a29-832e-b43cd3b7e4e6"
    response = request.put(url=url, json=data, scene=scene, parseToJson=False)
    return response


if __name__ == '__main__':
    login = login(username="testing@choiceform.com", password="cftesting")
    query_MdtableRes = query_Mdtable(scene="testing@choiceform.com")
    data_listA = []
    for i in query_MdtableRes.get("data"):
        number = i.get("id")
        data_listA.append(number)

    query_BuyRes = query_Buy(scene="testing@choiceform.com")
    # print(query_BuyRes)
    data_list = []
    for i in query_BuyRes.get("data"):
        value = i.get("cells").get("fldY4Rbislr5z8Cq3mY")
        idNum = i.get("id")
        data_list.append({"id": idNum, "value": value})
    getData_list = []
    for i in range(10):
        getData_list = []
        for i in range(5):
            numberA = random.choice(data_list)
            getData_list.append(numberA)
        data = {
            "cells": {
                "fldY4RaWclr5z8CtB-C": get_name(),
                "fldY4Rahclr5z8CCiiN": generate_mobile(),
                "fldY4Rapslr5z8CZvpg": {
                    "id": gender(),
                    "color": "#ff2bcd",
                    "name": "男"
                },
                "fldY4Ra-slr5z8CmZpY": Label(),
                "fldY4RbU8lr5z8C5O1Q": True,
                "fldY4RcHMlr5z8CwclP": getData_list,
                "fldY4RcXMlr5z8CRN4D": [random.choice(data_listA)],
                "fldY4Rbc8lr5z8CyjTe": "1987-11-28T15:00:00.000Z",
                "fldY4Rchclr5z8CmSzj": ""
            }
        }
        create_ClientRes = create_Client(data=data, scene="testing@choiceform.com")

    login = login(username="testing@choiceform.com", password="cftesting")
    # 获取节点
    # mail_getNodeRes = mail_getNode(scene="testing@choiceform.com")
    # 创建邮件
    data = {
        "id": "9b5071ab-a37a-4a29-832e-b43cd3b7e4e6",
        "name": "创建邮件服务的配置",
        "settings": {
            "key_id": "6385b14174a84547035e28ba",
            "key_secret": "key_secret",
            "provider": "aliyun"
        },
        "workspace_id": "6385b14174a84547035e28ba"
    }
    # mailCreateRes = mailCreate(data=data, scene="testing@choiceform.com")
    # 删除邮件
    # mailDeleteRes = mailDelete(scene="testing@choiceform.com")

    # # 获取邮件服务配置
    # mailGetRes = mailGet(scene="testing@choiceform.com")

    # 更新邮件配置
    dataA = {
        "name": "更新邮件服务的配置",
        "settings": {
            "key_id": "key_id",
            "key_secret": "key_secret",
            "provider": "aliyun"
        }
    }
    mailUpdateARes = mailUpdateA(data=dataA, scene="testing@choiceform.com")


