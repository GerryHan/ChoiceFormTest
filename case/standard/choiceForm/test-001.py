import random
import allure
import pytest

from lib.standard.globals.public.txSpaceApi import WorkspaceApi
from tools.printTool import zPrint
# 组织名称
organizationName = "自动化测试组织勿动" + str(random.randint(1, 1000))


@allure.feature("巧思科技")
@allure.story("测试空间")
@allure.suite("数据表")
@allure.title(f"组织-》空间-》数据表全流程")
@pytest.mark.smoke
def testExecCase():
    f"""查询表数据
    """
    try:
        # 前置
        preset()
        # 用例执行体
        case()

    finally:
        # 后置
        reset()


@allure.step("前置")
def preset():
    """
    用例内部前置方法名为
    :return:
    """


@allure.step("后置")
def reset():
    """
    用例内部后置方法名为
    :return:
    """


@allure.step("执行体")
def case():
    """
    执行体方法, 用例主要步骤
    :return:
    """
    with allure.step("新建一个组织"):
        dataOrganization = {
            "name": organizationName,  # 组织名称
            "data": {
                "name": "自动化测试组织",  # 组织名称
                "industry": "finance",  # 行业 finance(金融)  IT
                "size": "51-200",  # 规模 0-50 51-200 200+
                "rank": "",
                "department": ""
            }
        }
        # 获取组织ID
        res = WorkspaceApi.createOrganization(data=dataOrganization)
        tenant_id = res.get("data").get("id")

    with allure.step("新建一个空间"):
        dataSpace = {
            "name": "自动化测试空间勿动",
            "tenant_id": tenant_id
        }
        res = WorkspaceApi.createSpace(data=dataSpace)
        workspace_id = res.get("data").get("id")

    with allure.step("创建一张数据表A"):
        dataSheet = {
            "name": "自动化测试数据表勿动A",
            "fields": [
                {
                    "name": "名称",
                    "type": "text"
                }
            ],
            "workspace_id": workspace_id
        }
        res = WorkspaceApi.createDatasheet(data=dataSheet)
        datasheet_idA = res.get("data").get("id")
        # 获取默认的主字段的ID
        primary_field_id = res.get("data").get("primary_field_id")

    with allure.step("创建文本字段"):
        dataTextFiled = {
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
            "datasheet_id": datasheet_idA
        }
        res = WorkspaceApi.createTestField(data=dataTextFiled)
        # 获取文本字段ID
        text_id = res.get("data").get("id")

    with allure.step("创建单选字段"):
        dataRadioFiled = {
            "hidden": False,
            "name": "单选字段",
            "readonly": False,
            "required": True,
            "type": "single_select",
            "options": [
                {
                    "color": "#ff2b3a",
                    "default_checked": True,
                    "name": "自动化测试1号"
                },
                {
                    "color": "#00d046",
                    "default_checked": False,
                    "name": "自动化测试2号"
                },
                {
                    "color": "#9359ff",
                    "default_checked": False,
                    "name": "自动化测试3号"
                },
                {
                    "color": "#ff9900",
                    "default_checked": False,
                    "name": "自动化测试4号"
                }
            ],
            "datasheet_id": datasheet_idA
        }
        res = WorkspaceApi.createRadioField(data=dataRadioFiled)
        # 获取单选字段ID
        radio_id = res.get("data").get("id")
        # 获取颜色ID
        colorIdList = [i.get("id") for i in res.get("data").get("options") if i.get("id") is not None]

    with allure.step("创建数字字段"):
        dataNumFiled = {
            "hidden": False,
            "name": "数字字段",
            "readonly": True,
            "placeholder": "请填写整数",
            "required": True,
            "type": "number",
            "show_comma": False,
            "suffix": "",
            "prefix": "",
            "default_type": "value",
            "default_number": 50,
            "precision": 4,
            "min_number": -50,
            "max_number": 500,
            "datasheet_id": datasheet_idA
        }
        res = WorkspaceApi.createNumField(data=dataNumFiled)
        # 获取数字字段ID
        num_id = res.get("data").get("id")

    with allure.step("在数据表A中新增记录"):
        for i in range(20):
            # 主字段名称
            primaryName = "我是小飞人" + str(random.randint(1, 1000)) + "号"
            data = {
                "cells": {
                    primary_field_id: primaryName,
                    text_id: "自动化测试",
                    radio_id: {
                        "id": random.choice(colorIdList),
                        "color": "#ff2b3a",
                        "name": "自动化测试1号"
                    },
                    num_id: random.randint(-50, 100)
                }
            }
            WorkspaceApi.addRecord(data=data, datasheet_id=datasheet_idA)

    with allure.step("创建一张数据表B"):
        dataSheet = {
            "name": "自动化测试数据表勿动B",
            "fields": [
                {
                    "name": "名称",
                    "type": "text"
                }
            ],
            "workspace_id": workspace_id
        }
        res = WorkspaceApi.createDatasheet(data=dataSheet)
        datasheet_id = res.get("data").get("id")

    with allure.step("创建文本字段"):
        dataTextFiled = {
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
        WorkspaceApi.createTestField(data=dataTextFiled)

        with allure.step("创建单选字段"):
            dataRadioFiled = {
                "hidden": False,
                "name": "单选字段",
                "readonly": False,
                "required": True,
                "type": "single_select",
                "options": [
                    {
                        "color": "#ff2b3a",
                        "default_checked": True,
                        "name": "自动化测试1号"
                    },
                    {
                        "color": "#00d046",
                        "default_checked": False,
                        "name": "自动化测试2号"
                    },
                    {
                        "color": "#9359ff",
                        "default_checked": False,
                        "name": "自动化测试3号"
                    },
                    {
                        "color": "#ff9900",
                        "default_checked": False,
                        "name": "自动化测试4号"
                    }
                ],
                "datasheet_id": datasheet_id
            }
            WorkspaceApi.createRadioField(data=dataRadioFiled)

    with allure.step("创建单选字段"):
        dataRadioFiled = {
            "hidden": False,
            "name": "单选字段只读",
            "readonly": True,
            "required": True,
            "type": "single_select",
            "options": [
                {
                    "color": "#ff2b3a",
                    "default_checked": True,
                    "name": "自动化测试1号"
                },
                {
                    "color": "#00d046",
                    "default_checked": False,
                    "name": "自动化测试2号"
                },
                {
                    "color": "#9359ff",
                    "default_checked": False,
                    "name": "自动化测试3号"
                },
                {
                    "color": "#ff9900",
                    "default_checked": False,
                    "name": "自动化测试4号"
                }
            ],
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createRadioField(data=dataRadioFiled)

    with allure.step("创建多选字段"):
        dataMultipleFiled = {
            "hidden": False,
            "name": "多选字段",
            "readonly": True,  # 只读属性 （非只读为False）
            "required": False,
            "type": "multiple_select",
            "options": [
                {
                    "color": "#00d046",
                    "default_checked": False,
                    "name": "option1"
                },
                {
                    "color": "#ff9900",
                    "default_checked": True,
                    "name": "option2"
                },
                {
                    "color": "#9359ff",
                    "default_checked": False,
                    "name": "option3"
                },
                {
                    "color": "#e0e0e0",
                    "default_checked": False,
                    "name": "option4"
                }
            ],
            "min_selection": None,
            "max_selection": None,
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createMultipleField(data=dataMultipleFiled)

    with allure.step("创建数字字段"):
        dataNumFiled = {
            "hidden": False,
            "name": "数字字段",
            "readonly": False,
            "placeholder": "请填写整数",
            "required": True,
            "type": "number",
            "show_comma": False,
            "suffix": "",
            "prefix": "",
            "default_type": "value",
            "default_number": 50,
            "precision": 4,
            "min_number": -20,
            "max_number": 100,
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createNumField(data=dataNumFiled)

    with allure.step("创建复选字段"):
        dataCheckFiled = {
            "default_checked": False,
            "default_type": "value",
            "hidden": False,
            "name": "复选字段",
            "readonly": False,
            "required": False,
            "type": "checkbox",
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createNumField(data=dataCheckFiled)

    with allure.step("创建日期字段"):
        dataDateFiled = {
            "format": "YYYY-MM-DD HH:mm",
            "name": "日期字段",
            "readonly": False,
            "required": True,
            "has_time": True,
            "hidden": False,
            "type": "datetime",
            "allowed_weekdays": [
                1,
                2,
                3,
                4,
                5,
                6,
                7
            ],
            "allowed_time_ranges": [
            ],
            "start_time_type": "current",
            "default_type": "current",
            "end_time_type": "current",
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createDateField(data=dataDateFiled)

    with allure.step("创建关联记录字段"):
        # 查询被关联数据表的记录
        data = {
            "datasheet_id": datasheet_idA,
            "keyword": ""
        }
        queryDataSheetRes = WorkspaceApi.queryDataSheet(data)
        data_list = []
        for i in queryDataSheetRes.get("data"):
            number = i.get("id")
            data_list.append(number)

        getIdList = []
        for i in range(6):
            numberA = random.choice(data_list)
            getIdList.append(numberA)

        dataAssociatedFiled = {
            "hidden": False,
            "name": "关联记录字段",
            "readonly": False,
            "required": False,
            "type": "linked_record",
            "ref_datasheet_id": datasheet_idA,
            "single_linking": False,
            "default_ids": getIdList,
            "default_type": "value",
            "ui_settings": {
                "allowed_add_record_to_link": True
            },
            "datasheet_id": datasheet_id
        }
        res = WorkspaceApi.createAssociatedFiled(data=dataAssociatedFiled)
        # 获取关联记录字段id
        linked_field_id = res.get("data").get("id")

    with allure.step("创建他表字段"):
        idList = [text_id, primary_field_id, num_id, radio_id]
        dataOtherFiled = {
            "hidden": False,
            "name": "他表字段",
            "type": "lookup",
            "linked_field_id": linked_field_id,
            "ref_field_id": random.choice(idList),
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createOtherFiled(data=dataOtherFiled)

    with allure.step("创建圈选字段"):
        dataCircleFiled = {
            "hidden": False,
            "required": False,
            "name": "圈选字段",
            "type": "filter",
            # "default_filter_id": "fltZEJXXMlr51l33EUq",
            "default_type": "value",
            "ref_datasheet_id": datasheet_idA,
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createCircleFiled(data=dataCircleFiled)

    with allure.step("创建附件字段"):
        dataAnnexFiled = {
            "hidden": False,
            "required": True,
            "name": "附件字段",
            "type": "attachment",
            "ui_settings": {
                "file_sequence": "newest comes first",  # 文件顺序 (oldest comes first 旧的在最前面)
                "quantity_limit_min": 1,
                "quantity_limit_max": 10
            },
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createAnnexFiled(data=dataAnnexFiled)

    with allure.step("创建按钮字段"):
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
            "datasheet_id": datasheet_id
        }
        WorkspaceApi.createButtonFiled(data=dataButtonFiled)

