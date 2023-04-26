# -*- coding = utf-8 -*-
# @Time: 2023/11/30 16:36
# @Author: Gerry
# @File: login2.py
# @Software: PyCharm
import datetime
import json
import random
from config.globals import serverName
from config.globals.userInfo import UserInfo
from tools import request
from tools.common import date_time

user = UserInfo()
txapi = serverName.txapi
tenant_id = "6385b14174a84547035e28ba"


def generate_mobile():
    """随机生成一个手机号码。。    1[3,5,8,9] + 9"""
    phone = '1' + random.choice(["3", "5", "7", "8", "9"])
    for i in range(9):
        num = random.randint(1, 9)
        phone += str(num)
    return phone


def generate_poNum():
    """随机生成一个订单号。。    1[3,5,8,9] + 9"""
    poNum = 'XSDD' + date_time(fmt="%Y%m%d%H%M%S")
    for i in range(2):
        num = random.randint(1, 9)
        poNum += str(num)
    return poNum


def gender():
    """随机取一个性别。。"""
    gender_random = random.choice(["optY8ExZ8lr51tlN1oP", "optY8ExZ8lr51tlN1oQ"])
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
                "id": "optY8Expslr51tlmcj9",
                "color": "#A3A3A3",
                "name": "低消费"
            },
            {
                "id": "optY8Expslr51tlmcj_",
                "color": "#A3A3A3",
                "name": "多次复购"
            },
            {
                "id": "optY8Expslr51tlmcj-",
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
    url = f"{txapi}/records?page=1&page_size=1000"
    data = {"datasheet_id": "dtsY8Evx8lr51tlyyWj",
            "keyword": ""}
    data_dict = request.post(url=url, json=data, scene=scene)
    return data_dict


def query_Buy(scene):
    # 购买记录接口
    url = f"https://txapi.choiceform.io/api/v1/records?page=1&page_size=1000"
    data = {"datasheet_id": "dtsY8Evz8lr51tlyvbb",
            "keyword": ""}
    data_dict = request.post(url=url, json=data, scene=scene)
    return data_dict


def create_Client(data, scene):
    """
    :param data:
    :param scene:
    :return:
    """
    # 创建数据表
    url = f"https://txapi.choiceform.io/api/v1/datasheets/dtsY8Ev2clr51tlRPqN/records"
    data_dict = request.post(url=url, json=data, scene=scene)
    return data_dict


def create_Buy(data, scene):
    """
    :param data:
    :param scene:
    :return:
    """
    # 创建购买记录
    url = f"https://tx.choiceform.io/api/tx/v1/datasheets/dtsY8Evz8lr51tlyvbb/records"
    data_dict = request.post(url=url, json=data, scene=scene)
    return data_dict


def createSpace(name="创建空间", scene="testing@choiceform.com"):
    """
    :param name:
    :param scene:
    data = {
    name: "测试空间1号"，
    tenant_id: "6385b14174a84547035e28ba"
    }
    :return:
    """
    # 新建空间
    url = f"{txapi}/workspaces"
    data = {
        "name": name,
        "tenant_id": tenant_id
    }
    res = request.post(url=url, json=data, scene=scene, parseToJson=False)
    assert res.status_code == 201, "创建空间失败"
    return res


if __name__ == '__main__':
    login = login(username="testing@choiceform.com", password="cftesting")
    query_MdtableRes = query_Mdtable(scene="testing@choiceform.com")
    data_listA = []
    for i in query_MdtableRes.get("data"):
        number = i.get("id")
        data_listA.append(number)

    query_BuyRes = query_Buy(scene="testing@choiceform.com")
    data_list = []
    for i in query_BuyRes.get("data"):
        value = i.get("cells").get("fldY8Evz8lr51tlyvba")
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
                "fldY8Ev2clr51tlRPqM": get_name(),
                "fldY8ExR8lr51tlrTJV": generate_mobile(),
                "fldY8ExZ8lr51tlN1oO": {
                    "id": gender(),
                    "color": "#ff2bcd",
                    "name": "男"
                },
                "fldY8Expslr51tlmcj8": Label(),
                "fldY8ExtMlr51tlEpfO": True,
                "fldY8EyBMlr524QxwB6": getData_list,
                "fldY8EyLslr524QJ4-i": [random.choice(data_listA)],
                "fldY8EzOslr524QEpwB": getData_list,
                "fldY8EzvMlr524QJeCO": [random.choice(data_listA)],
                "fldY8Ex28lr524Qsx9O": "1987-11-28T15:00:00.000Z",
                "fldY4Rchclr5z8CmSzj": ""
            }
        }
        create_ClientRes = create_Client(data=data, scene="testing@choiceform.com")

        data = {
                "cells": {
                    "fldY8Evz8lr51tlyvba": generate_poNum(),
                    "fldY8Ew9clr51tlJS-z": random.randint(100, 10000),
                    "fldY8EyBMlr524QxwB7": [],
                    "fldY8EzvMlr524QJeCN": [],
                    "fldY8ExDslr51tlw2-v": "2023-01-13T13:15:00.000Z"
                }
            }
        create_BuyRes = create_Buy(data=data, scene="testing@choiceform.com")


recZEI7Oslr51l3r_T9
