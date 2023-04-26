# -*- coding = utf-8 -*-
# @Time: 2023/3/26 17:07
# @Author: Gerry
# @File: standardAccInfo.py
# @Software: PyCharm
from config.globals.environment import env

mockUrl = "https://tx.choiceform.io"

if env == "dev":
    # ************************** 开发环境协议域名 **************************
    protocol = "https"
    host = "txapi.choiceform.io"
    port = ""
    secHost = ""

    # ************************** 正式环境redis配置 **************************
    redisHostname = ""
    redisPwd = ""


# elif env == "test" or env == "zhenYunTest":
#     # ************************** 测试环境协议域名 **************************
#     protocol = "https"
#     host = "test.isrm.going-link.com"
#     port = ""
#     secHost = ""
#
#     # ************************** 测试环境redis配置 **************************
#     redisHostname = "192.168.4.114"
#     redisPwd = "PUAWt!Lb77u3dvm8"


# 初始化


# 主账号
# 注意: 这组不能和其他组同时登录
# 注意: 这组不能和其他组同时登录
# 注意: 这组不能和其他组同时登录

# 测试一组
dev1 = {
    "groupName": "dev1",
    "purAccNum": "testing@choiceform.com",
}



