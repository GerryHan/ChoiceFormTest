# -*- coding: utf-8 -*-
# @Time: 2023/2/21 15:49
# @Author: Gerry
# @File: assertTool.py
# @Software: PyCharm
import copy
import inspect
import json
import re
import time

import allure

from tools.printTool import zPrint
from tools.common import sortList


@allure.step("数据断言")
def assertData(function, msg, *args, **kwargs):
    """
    使用说明：当要查询的字段值是列表的时候不适用此方法
    :param function: 函数名
    :param msg: 断言描述
    :param args: 方法中的参数
    :param kwargs: 键值对，键为【参数名】；值为：【预期结果】--type：list
    :return:
    """
    response = function(*args)
    string = str(response)
    result = []
    for key, value in kwargs.items():
        i = 1
        if value is not None:
            pattern = key + r"': (.*?)[,\]\}]"
            actualValueList = re.findall(pattern, string)
            if "'" in actualValueList[0]:
                actualValueList = [i.replace("'", "") for i in actualValueList]
            elif "." in actualValueList[0]:
                actualValueList = [float(i) for i in actualValueList]
            else:
                actualValueList = [int(i) for i in actualValueList]
            # if "Quantity" in key or "Amount" in key or "Flag" in key or "quantity" in key or "Price" in key:
            for actualValue, assertValue in zip(actualValueList, value):
                with allure.step("断言{}: {}，断言字段:{}，期望结果: {}， 实际结果: {}".format(i, msg, key, assertValue, actualValue)):
                    try:
                        assert actualValue == assertValue
                    except:
                        result.append({"期望结果": assertValue, "实际结果": actualValue, "断言字段": key})
                        # logging.error("{0}测试用例执行失败，{1}:期望结果错误，期望结果是{2},实际结果是{3}".format(msg + "测试用例执行失败", key, value, response[key]))
                i += 1

        # else:
        #     with allure.step("未断言的字段：{}".format(key)):
        #         pass

    return result


def assertAsync(request, times=10, polling=3, sortFlag=False, key="", specChar="",  **kwargs):
    """
    异步接口轮询断言,非异步接口不建议使用,太多查询次数影响执行效率
    @param request: 请求方法
    @param times: 默认查询次数（默认30次）
    @param polling: 轮询时间（默认1秒）
    @param sortFlag: 是否需要排序单号
    @param key: 需排序的键
    @param specChar: 特殊字符过滤
    @param kwargs: 方法入参和校验字段
    @return:
    """
    assert callable(request), NameError(request.__name__)
    func = inspect.signature(request)
    request_params, assert_params = dict(), dict()
    for name, value in kwargs.items():
        for k, v in func.parameters.items():
            if name == k:
                request_params[name] = value
            else:
                if name not in func.parameters.keys():
                    assert_params[name] = value
    for _ in range(times):
        try:
            response = request(**request_params)
            # 校验异步接口可以查询到列表数据
            assert response, AssertionError(response)
            if sortFlag:
                response = sortList(data=response, key=key, specChar=specChar)
            assertCommon(response=response, **assert_params)
            break
        except AssertionError:
            time.sleep(polling)
    else:
        raise AssertionError(f"{request}\n请求参数: {request_params}\n校验参数: {assert_params}\n")
    return response


@allure.step("数据断言")
def assertCommon(response, **kwargs):
    """
    使用说明：当要查询的字段值是列表或字典的时候不适用此方法
    :param response:接口返回值
    :param kwargs: 键值对，键为【参数名】；值为：【预期结果】--type：list
    :return:
    """
    string = str(response)
    result = []
    for key, value in kwargs.items():
        if value is None:
            continue
        # i = 1
        pattern = "'" + key + r"': (.*?)[,\]\}]"
        actualValueList = re.findall(pattern, string)
        # if isinstance(value, list) and None in value:
        #     pass
        # else:
        actualValueList = [i for i in actualValueList if i != 'None']
        # print("actualValueList............", actualValueList)
        if len(actualValueList) == 0:
            assert False, f"返回值中找不到{key}键"
        if "'" in actualValueList[0]:
            actualValueList = [i.replace("'", "") for i in actualValueList]
        else:
            actualValueList = [float(i) if "." in i else int(i) for i in actualValueList]
        # elif "." in actualValueList[0]:
        #     actualValueList = [float(i) for i in actualValueList]
        # else:
        #     try:
        #         actualValueList = [int(i) for i in actualValueList]
        #     except:
        #         assert False, "传参类型传错了"
        # if "Quantity" in key or "Amount" in key or "Flag" in key or "quantity" in key or "Price" in key:
        if type(value) is not list:
            try:
                assert actualValueList[0] == value
                with allure.step("断言成功: 断言字段:{}，期望结果: {} = 实际结果: {}".format(key, value, actualValueList[0])):
                    pass
            except:
                result.append({"期望结果": value, "实际结果": actualValueList[0], "断言字段": key})
                try:
                    with allure.step("断言失败: 断言字段:{}，期望结果: {} != 实际结果: {}".format(key, value, actualValueList[0])):
                        assert False
                except:
                    zPrint("断言失败: 断言字段:{}，期望结果: {} != 实际结果: {}".format(key, value, actualValueList[0]))
                # logging.error("{0}测试用例执行失败，{1}:期望结果错误，期望结果是{2},实际结果是{3}".format(msg + "测试用例执行失败", key, value, response[key]))
            # i += 1
        else:
            for actualValue, assertValue in zip(actualValueList, value):
                try:
                    assert actualValue == assertValue
                    with allure.step("断言成功: 断言字段:{}，期望结果: {} = 实际结果: {}".format(key, assertValue, actualValue)):
                        pass
                except:
                    result.append({"期望结果": assertValue, "实际结果": actualValue, "断言字段": key})
                    try:
                        with allure.step("断言失败: 断言字段:{}，期望结果: {} != 实际结果: {}".format(key, assertValue, actualValue)):
                            assert False
                    except:
                        zPrint("断言失败: 断言字段:{}，期望结果: {} != 实际结果: {}".format(key, assertValue, actualValue))

                    # logging.error("{0}测试用例执行失败，{1}:期望结果错误，期望结果是{2},实际结果是{3}".format(msg + "测试用例执行失败", key, value, response[key]))
                # i += 1

        # else:
        #     with allure.step("未断言的字段：{}".format(key)):
        #         pass
    # if len(result) > 0:
    #     zPrint(jsonData=result)
    assert len(result) == 0


def assertQuery(fun, num, sec, *args):
    for i in range(num):
        responseQuery = fun(*args)
        if len(responseQuery["content"]) == 0:
            time.sleep(sec)
    else:
        assert False, "未查询到数据"


def getValueList(response, key):
    string = str(response)
    pattern = key + r"': (.*?)[,\]\}]"
    actualValueList = re.findall(pattern, string)
    actualValueList = [i for i in actualValueList if i != 'None']
    if len(actualValueList) == 0:
        assert False, "返回值中找不到该键"
    if "'" in actualValueList[0]:
        actualValueList = [i.replace("'", "") for i in actualValueList]
    else:
        actualValueList = [float(i) if "." in i else int(i) for i in actualValueList]
    # elif "." in actualValueList[0]:
    #     actualValueList = [float(i) for i in actualValueList]
    # else:
    #     actualValueList = [int(i) for i in actualValueList]
    return actualValueList


# 递归方法取值
def getValue(response, obj, default=None):
    for k, v in response.items():
        if k == obj:
            return v
        elif type(v) is list:
            for i in v:
                if type(i) is dict:
                    re = getValue(i, obj)
                    if re is not default:
                        return re
        elif type(v) is dict:
            re = getValue(v, obj)
            if re is not default:
                return re


result = []


# 递归方法断言
def getValueAssert(dictResponse, key, value):
    for d, v in dictResponse.items():
        if d == key:
            with allure.step("断言字段:{}，期望结果: {}， 实际结果: {}".format(key, value, v)):
                try:
                    assert v == value
                except:
                    result.append({"断言字段:{}，期望结果: {}， 实际结果: {}".format(key, value, v)})
            return v
        elif type(v) is list:
            for i in v:
                if type(i) is dict:
                    return1 = getValue(i, key, value)
        elif type(v) is dict:
            return2 = getValue(v, key, value)
    if return1 is None and return2 is None:
        print("找不到键")
        raise
    assert len(result) == 0


def assertAsyncCustomize(request, times=10, polling=1,  **kwargs):
    """
    用于自定义封装的校验方法，实现异步校验
    异步接口轮询断言,非异步接口不建议使用,太多查询次数影响执行效率
    @param request: 请求方法
    @param times: 默认查询次数（默认10次）
    @param polling: 轮询时间（默认1秒）
    @param kwargs: 方法入参和校验字段
    @return:
    """
    assert callable(request), NameError(request.__name__)
    for _ in range(times):
        try:
            request(**kwargs)
            break
        except AssertionError:
            time.sleep(polling)
    else:
        raise AssertionError(f"{request}\n校验参数: {kwargs}\n")