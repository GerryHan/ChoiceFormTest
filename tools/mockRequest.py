# -*- coding = utf-8 -*-
# @Time: 2023/2/21 15:16
# @Author: Gerry
# @File: mockRequest.py
# @Software: IntelliJ IDEA
import json
import allure
from tools.common import date_time
from config.globals.environment import env
import requests
from config.globals.userInfo import UserInfo
from config.globals import baseinfo


HTTP_TIMEOUT_TIME = 120  # http请求等待超时时间  （秒）
user = UserInfo()


def addInfoToAllure(response):
    """
    添加请求响应信息到allure
    :param response: 请求响应数据
    :return:
    """
    info = [
        f"调用时间:  {date_time(fmt='%Y-%m-%d %H:%M:%S')}",
        f"请求链接:  {response.request.url}",
        f"请求方法:  {response.request.method}",
        f"响应码:  {str(response.status_code)}",
        f"请求头:  {str(str(response.request.headers))}"
    ]
    try:
        info.append("Response Body:\n" + json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.decoder.JSONDecodeError:
        info.append("Response Body:\n" + response.text)

    if response.request.body is not None:
        if isinstance(response.request.body, bytes):
            # 将json类型Post数据unicode转为中文字符串
            requestBody = response.request.body.decode('unicode-escape', errors="ignore")
            try:
                info.append("Body:\n" + json.dumps(json.loads(requestBody), indent=4, ensure_ascii=False))
            except json.decoder.JSONDecodeError:
                info.append("Body:\n" + requestBody)
        else:
            info.append("Body:\n" + response.request.body)

    allure.attach("\n\n".join(info), "Request&Response")


def mockRequest(method, url, scene, **kwargs):
    """
    网络请求
    :return:
    """
    # 是否解析
    parseToJson = True
    if "parseToJson" in kwargs:
        parseToJson = kwargs.get("parseToJson")
        kwargs.pop("parseToJson")

    # 获取headers
    headers = {"srm-auto-test": "true"}
    if "headers" in kwargs:
        resHeaders = kwargs.get("headers")
        headers.update(resHeaders)
        kwargs.pop("headers")

    # 获取token
    token = user.getMockToken(scene=scene)
    if token is not None:
        headers.update(mock=token)

    response = requests.request(method=method, url=baseinfo.mockUrl + url, headers=headers, timeout=HTTP_TIMEOUT_TIME, **kwargs)
    addInfoToAllure(response)

    def parseRes(res):
        try:
            dic: object = res.json()
            if isinstance(dic, dict) and dic.get("failed") is True:
                try:
                    with allure.step("*************请求报错接口*************"):
                        # 添加请求失败在报告中的标记
                        addInfoToAllure(res)
                        assert False
                except:
                    pass
            return dic
        except:
            pass

    if parseToJson:
        return parseRes(res=response)
    else:
        parseRes(res=response)
        return response


def get(url, scene, params=None, parseToJson=True, **kwargs):
    if env == "test":
        requestUrl = url + "&environment=test"
    elif env == "prod":
        requestUrl = url + "&environment=prod"
    else:
        assert False, "待补充"
    return mockRequest(method='get', scene=scene, url=requestUrl, params=params, parseToJson=parseToJson, **kwargs)


def post(url, scene, data=None, json=None, parseToJson=True, **kwargs):
    if env == "test":
        if json is not None and isinstance(json, dict):
            json.update(environment="test")
        elif json is not None and isinstance(json, list):
            for item in json:
                item.update(environment="test")
    elif env == "prod":
        if json is not None and isinstance(json, dict):
            json.update(environment="prod")
        elif json is not None and isinstance(json, list):
            for item in json:
                item.update(environment="prod")
    else:
        assert False, "待补充"
    return mockRequest(method='post', scene=scene, url=url, data=data, json=json, parseToJson=parseToJson, **kwargs)
