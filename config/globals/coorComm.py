# -*- coding = utf-8 -*-
# @Time: 2023/3/23 10:56
# @Author: Gerry
# @File: coorComm.py
# @Software: PyCharm
from config.globals.environment import env

if env == "dev":
    from config.standard.choiceFormination.choiceFormComms.coorDev import *
    from config.standard.choiceFormination.choiceFormComms.coorPre import *
# elif env == "test":
#     from config.standard.choiceFormination.choiceFormComms.coorTest import *
else:
    from config.standard.choiceFormination.choiceFromCommon import *
