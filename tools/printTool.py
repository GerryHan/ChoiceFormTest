# -*- coding = utf-8 -*-
# @Time: 2023/2/5 14:24
# @Author: Gerry
# @File: printTool.py
# @Software: PyCharm
from config.globals.baseinfo import isShowPrint
import json
import time
from tools.logger import Logger


def zPrint(prama="", *args, **kwargs):
    """
    自定制打印
    :return:
    """
    if isShowPrint:
        # Logger().info(msg="")
        # time.sleep(0.000001)
        jsonData = {}
        if "jsonData" in kwargs:
            jsonData = kwargs["jsonData"]
            kwargs.pop("jsonData")
            print(prama, json.dumps(jsonData, indent=4, ensure_ascii=False, sort_keys=True),
                  args if len(args) > 0 else "", kwargs if len(kwargs) > 0 else "")
        else:
            print(prama, args if len(args) > 0 else "", kwargs if len(kwargs) > 0 else "")
    else:
        pass


# if __name__ == '__main__':
#     zPrint(prama="hdhdh")