# -*- coding = utf-8 -*-
# @Time: 2023/2/21 16:29
# @Author: Gerry
# @File: conftest.py
# @Software: PyCharm
import json

from globalImportBase import pytest, date_time, UserInfo, zPrint
from tools import request
from filelock import FileLock


@pytest.fixture(scope="session", autouse=True)
def globalPresetAndReset():
    """
    全局前置
    :return:
    """
    zPrint("\n全局前置----开始----\n")
    zPrint(f"正在登录请耐心等待...", date_time(fmt="%Y-%m-%d %H:%M:%S"))
    with FileLock("session.lock"):
        login(username="testing@choiceform.com", password="cftesting")

        zPrint("登录完毕...", date_time(fmt="%Y-%m-%d %H:%M:%S"))

    # # 链接数据库
    # if isConnectDB is True:
    #     DBTool.openDB()

    yield

    # # 插入结束时间
    # DBTool.insertEndTimeSql(suiteName=suiteName)
    #
    # # 关闭数据库
    # if isConnectDB is True:
    #     DBTool.closeDB()
    zPrint("\n全局后置----结束----\n")


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

