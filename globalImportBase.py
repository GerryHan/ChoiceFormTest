# -*- coding = utf-8 -*-
# @Time: 2023/1/27 16:41
# @Author: Gerry
# @File: globalImportBase.py
# @Software: PyCharm

# 注意此文件不能导入lib文件夹非公有的文件,导入tools的东西时注意循环导入

import re
import pytest
import time
import allure
import json
import redis
import threading
import random
import os
import datetime
import copy

from tools import request, mockRequest
from tools.common import *
# from tools.common import timestamp, cleanNoneFromDict, getPrecision
# from tools.common import date_time, days, strToDate, executeTime
# from tools.common import randomNumNotRepeat
# from tools.common import changePath
# from tools.common import sleep
from tools.redisTool import searchRedisCode, searchRedisCode1
from tools.rsaTool import encrypt
# from tools.common import random_string
# from tools.common import confirmUnique
# from tools.common import noneToEmptyString
# from tools.common import sortDictInList
# from tools.common import sortDict
from tools.printTool import zPrint
import tools.assertTool as AssertTool
# from tools.common import writeExcelData
# from tools.common import saveExportFile, deleteFile, saveUrlExportFile, changeNonString
import tools.operaterDb as operaterDb

from config.globals import baseinfo
from config.globals.userInfo import UserInfo, AccountInfo
from config.globals import coorComm
