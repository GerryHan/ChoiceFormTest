# -*- coding = utf-8 -*-
# @Time: 2023/04/01 16:36
# @Author: Gerry
# @File: txSpaceApi.py
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
scene = "testing@choiceform.com"


class WorkspaceApi:

    @staticmethod
    def queryDataSheet(data, scene=scene):
        """
        :param data:
        :param scene:
        :return:
        data = {"datasheet_id": "dtsY8Evx8lr51tlyyWj",
        "keyword": ""}
        """
        # 查询客户记录
        url = f"{txapi}/records?page=1&page_size=1000"
        data_dict = request.post(url=url, json=data, scene=scene)
        return data_dict

    @staticmethod
    def query_Buy(scene=scene):
        # 购买记录接口
        url = f"https://txapi.choiceform.io/api/v1/records?page=1&page_size=1000"
        data = {"datasheet_id": "dtsY8Evz8lr51tlyvbb",
                "keyword": ""}
        data_dict = request.post(url=url, json=data, scene=scene)
        return data_dict

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def createOrganization(data, scene="testing@choiceform.com"):
        """
        :param scene:
        :param data:
        data = {
            "name": "测试组织1号",  # 组织名称
            "data": {
                "name": "测试组织1号",  # 组织名称
                "industry": "finance",  # 行业 finance(金融)  IT
                "size": "51-200",  # 规模 0-50 51-200 200+
                "rank": "",
                "department": ""
            }
        }
        :return:
        """
        # 新建组织
        url = f"https://portal.choiceform.io/api/orgs"
        res = request.post(url=url, json=data, scene=scene)
        assert res.get("msg") == "创建成功", "创建自动化组织失败"
        return res

    @staticmethod
    def createSpace(data, scene=scene):
        """
        :param data:
        :param scene:
        data = {
        name: "测试空间1号"，
        tenant_id: "tenant_id"  组织id
        }
        :return:
        """
        # 新建空间
        url = f"{txapi}/workspaces"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "空间创建失败"
        return res

    @staticmethod
    def createDatasheet(data, scene=scene):
        """
        创建数据表
        :param data:
        :param scene:
        :return:
        data = {
            "name": "自动化测试数据表",
            "fields": [
                {
                    "name": "名称",
                    "type": "text"
                }
            ],
            "workspace_id": "wksZD-hNMlr5zKfa5NZ"
        }
        """
        # 创建数据表
        url = f"{txapi}/datasheets"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建数据表失败"
        return res

    @staticmethod
    def addRecord(data, datasheet_id, scene=scene):
        """
        新增记录
        :param data:
        :param scene:
        :param datasheet_id:
        :return:
        data = {
            "cells":{
                "fldZEIoHslr51l317tg":"我是小飞人",
                "fldZEIoHslr51l317ti":"自动化测试",
                "fldZEIoHslr51l317tj":{
                    "id":"optZEIoHslr51l317tk",
                    "color":"#ff2b3a",
                    "name":"自动化测试1号"
                },
                "fldZEIoHslr51l317to":50
            }
        }
        """
        # 新增记录
        url = f"{txapi}/datasheets/{datasheet_id}/records"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "新增记录失败"
        return res

    @staticmethod
    def createTestField(data, scene=scene):
        """
        创建文本字段
        :param data:
        :param scene:
        :return:
        dataFiled = {
            "name": "文本字段",
            "readonly": False,
            "required": True,
            "hidden": False,
            "type": "text",
            "min_chars": None,
            "max_chars": None,
            "multiple_lines": False,
            "default_text": "自动化测试",
            "default_type": "value",
            "unique": False,
            "placeholder": "请输入值",
            "datasheet_id": datasheet_id
        }
        """
        # 创建文本字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建文本字段失败"
        return res

    @staticmethod
    def createRadioField(data, scene=scene):
        """
        创建单选字段
        :param data:
        :param scene:
        :return:
        dataRadioFiled = {
            "hidden":false,
            "name":"单选字段",
            "readonly":false,
            "required":true,
            "type":"single_select",
            "options":[
                {
                    "color":"#ff2b3a",
                    "default_checked":true,
                    "name":"自动化测试1号"
                },
                {
                    "color":"#00d046",
                    "default_checked":false,
                    "name":"自动化测试2号"
                },
                {
                    "color":"#9359ff",
                    "default_checked":false,
                    "name":"自动化测试3号"
                },
                {
                    "color":"#ff9900",
                    "default_checked":false,
                    "name":"自动化测试4号"
                }
            ],
            "datasheet_id":"dtsZD-17Mlr51Ux2gQg"
        }
        """
        # 创建单选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建单选字段失败"
        return res

    @staticmethod
    def createMultipleField(data, scene=scene):
        """
        创建多选字段
        :param data:
        :param scene:
        :return:
        dataMultipleFiled = {
            "hidden":false,
            "name":"多选字段",
            "readonly":true,
            "required":false,
            "type":"multiple_select",
            "options":[
                {
                    "color":"#00d046",
                    "default_checked":false,
                    "name":"option1"
                },
                {
                    "color":"#ff9900",
                    "default_checked":true,
                    "name":"option2"
                },
                {
                    "color":"#9359ff",
                    "default_checked":false,
                    "name":"option3"
                },
                {
                    "color":"#e0e0e0",
                    "default_checked":false,
                    "name":"option4"
                }
            ],
            "min_selection":null,
            "max_selection":null,
            "datasheet_id":"dtsZD-4x8lr51UxepHI"
        }
        """
        # 创建多选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建多选字段失败"
        return res

    @staticmethod
    def createNumField(data, scene=scene):
        """
        创建数字字段
        :param data:
        :param scene:
        :return:
        dataNumFiled = {
            "hidden":false,
            "name":"数字字段",
            "readonly":false,
            "placeholder":"请填写整数",
            "required":true,
            "type":"number",
            "show_comma":false,
            "suffix":"",
            "prefix":"",
            "default_type":"value",
            "default_number":50,
            "precision":4,
            "min_number":-20,
            "max_number":100,
            "datasheet_id":"dtsZEECs8lr5xschzAO"
        }
        """
        # 创建数字字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建数字字段失败"
        return res

    @staticmethod
    def createCheckField(data, scene=scene):
        """
        创建复选字段
        :param data:
        :param scene:
        :return:
        dataCheckFiled = {
            "default_checked":true,
            "default_type":"value",
            "hidden":false,
            "name":"复选字段",
            "readonly":false,
            "required":false,
            "type":"checkbox",
            "datasheet_id":"dtsZEECs8lr5xschzAO"
        }
        """
        # 创建复选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建复选字段失败"
        return res

    @staticmethod
    def createDateField(data, scene=scene):
        """
        创建日期字段
        :param data:
        :param scene:
        :return:
        dataDateFiled = {
            "format":"YYYY-MM-DD HH:mm",
            "name":"日期字段",
            "readonly":false,
            "required":true,
            "has_time":true,
            "hidden":false,
            "type":"datetime",
            "allowed_weekdays":[
                1,
                2,
                3,
                4,
                5,
                6,
                7
            ],
            "allowed_time_ranges":[

            ],
            "start_time_type":"current",
            "default_type":"current",
            "end_time_type":"current",
            "datasheet_id":"dtsZEECs8lr5xschzAO"
        }
        """
        # 创建复选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建日期字段失败"
        return res

    @staticmethod
    def createAssociatedFiled(data, scene=scene):
        """
        创建关联记录字段
        :param data:
        :param scene:
        :return:
        dataAssociatedFiled = {
            "hidden":false,
            "name":"关联记录字段",
            "readonly":false,
            "required":false,
            "type":"linked_record",
            "ref_datasheet_id":"dtsZEI7Nslr51l3Bt0k",
            "single_linking":false,
            "default_ids":[
                "recZEI7Oslr51l3r_T9",
                "recZEI7Oslr51l3r_T8",
                "recZEI7Oslr51l3r_T7",
                "recZEI7Oclr51l3v_XO",
                "recZEI7Oclr51l3v_XN"
            ],
            "default_type":"value",
            "ui_settings":{
                "allowed_add_record_to_link":true
            },
            "datasheet_id":"dtsZEI7Oslr51l3r_T_"
        }
        """
        # 创建复选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建关联记录字段失败"
        return res

    @staticmethod
    def createOtherFiled(data, scene=scene):
        """
        创建他表字段
        :param data:
        :param scene:
        :return:
        dataOtherFiled = {
            "hidden":false,
            "name":"他表字段",
            "type":"lookup",
            "linked_field_id":"fldZEJBNslr51l3aCpe",
            "ref_field_id":"fldZEJBMslr51l3e8NX",
            "datasheet_id":"dtsZEJBNslr51l3aCpK"
        }
        """
        # 创建复选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建他表字段失败"
        return res

    @staticmethod
    def createCircleFiled(data, scene=scene):
        """
        创建圈选字段
        :param data:
        :param scene:
        :return:
        dataCircleFiled = {
            "hidden": False,
            "required": False,
            "name": "圈选字段",
            "type": "filter",
            "default_filter_id": "fltZEJXXMlr51l33EUq",
            "default_type": "value",
            "ref_datasheet_id": datasheet_idA,
            "datasheet_id": datasheet_id
        }
        """
        # 创建复选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建圈选字段失败"
        return res

    @staticmethod
    def createAnnexFiled(data, scene=scene):
        """
        创建附件字段
        :param data:
        :param scene:
        :return:
        dataAnnexFiled = {
            "hidden":false,
            "required":true,
            "name":"附件字段",
            "type":"attachment",
            "ui_settings":{
                "file_sequence":"newest comes first",
                "quantity_limit_min":1,
                "quantity_limit_max":10
            },
            "datasheet_id":"dtsZEJYhMlr51l3Kp1m"
        }
        """
        # 创建复选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建附件字段失败"
        return res

    @staticmethod
    def createButtonFiled(data, scene=scene):
        """
        创建附件字段
        :param data:
        :param scene:
        :return:
        dataButtonFiled = {
            "name": "按钮字段",
            "label": "我是按钮字段",
            "type": "button",
            "style": {
                "color": "#FFFFFF",
                "background": "#DB2424"
            },
            "interaction": "execution",
            "confirmation_settings": None,
            "binding": None,
            "datasheet_id": "datasheet_id"
        }
        """
        # 创建复选字段
        url = f"{txapi}/fields"
        res = request.post(url=url, json=data, scene=scene)
        assert isinstance(res.get("data"), dict) and res.get("data") is not None, "创建按钮字段失败"
        return res
