# -*- coding = utf-8 -*-
# @Time: 2023/1/29 18:29
# @Author: Gerry
# @File: redisTool.py
# @Software: PyCharm
import redis
from config.globals.baseinfo import redisHostname, redisPwd
import requests
import re

session = requests.session()
username = "30280"  # 账号
password = "Zy#88888"  # 密码
token = ""
sessionId = ""
route = ""

# 登录
def login():
    """
    :return:
    """
    data = {
        "username": username,
        "password": password
    }
    csrfToken = 'pMMCWYGfdrf6cfGDkT0OWLAAneRW6DngktOz0RzjVFltljijgrtJK5sHf6AdiL5h'
    url = f"https://archery.going-link.net/authenticate/"
    res = session.request(method="post", url=url, data=data, headers={"Cookie": "csrftoken=%s" % csrfToken, "X-CSRFToken": csrfToken})
    cookie = res.headers.get("Set-Cookie")
    assert cookie is not None, "cookie 为空"
    assert re.search("csrftoken=(.*?);", cookie) is not None, "csrfToken 为空"
    assert re.search("sessionid=(.*?);", cookie) is not None, "sessionid 为空"
    assert re.search("route=(.*?);", cookie) is not None, "route 为空"
    t = re.search("csrftoken=(.*?);", cookie).group(1)
    s = re.search("sessionid=(.*?);", cookie).group(1)
    r = re.search("route=(.*?);", cookie).group(1)
    global token, sessionId, route
    token = t
    sessionId = s
    route = r

# 查询sql审计平台

def searchRedisCode(key, db=1, env="test"):
    """
    查询审计平台
    :param env: 环境
    :param key:
    :param db:
    :return:
    """

    # 登录
    login()

    sql = f"""
    get hiam:captcha:user_type_p:default:code:{key}
    """

    if env == "prod":
        instanceName = "SaaS-SRM-生产环境-缓存"
    else:
        instanceName = "SaaS-SRM-测试环境-缓存"

    url = "https://archery.going-link.net/query/"
    queryData = {
        "instance_name": instanceName,
        "db_name": db,
        "sql_content": sql,
        "limit_num": 0
    }
    h1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": f"route={route}; csrftoken={token}; sessionid={sessionId}",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRFToken": token,
        "X-Requested-With": "XMLHttpRequest"
    }
    res = session.request(method="post", url=url, data=queryData, headers=h1)
    dic = res.json()
    assert isinstance(dic, dict), "数据结构有误"
    resNums = dic.get("data").get("rows")
    assert len(resNums) > 0, "未查到验证码"
    assert len(resNums[0]) > 0, "未查到验证码"
    smsCode = resNums[0][0].split('_')[0]
    print(smsCode)
    return smsCode


# 直接访问redis
def searchRedisCode1(key, port=6379, db=1):
    """
    查询验证码
    :param db:
    :param port:
    :param key: 发短信时生成的key,有时间限制
    :return: 验证码
    """

    # 2.链接redis
    pool = redis.StrictRedis(
        host=redisHostname,
        port=port,
        db=db,
        password=redisPwd,
        decode_responses=True)
    key1 = "hiam:captcha:user_type_p:default:code:" + key
    # 3.根据key获取验证码
    code = pool.get(key1)
    if code is None:
        return "验证码失败"
    else:
        # 分割获取验证码
        return code.split('_')[0]

# if __name__=="__main__":
#     print(searchRedisCode(key="5207410ec9e84defb66325969f5a3638", port=6379, db=1))


