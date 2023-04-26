import requests
from requests import sessions, Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from config.globals import baseinfo, serverName
from config.globals.userInfo import UserInfo
import allure
import json
from tools.common import date_time
from tools.operaterDb import DBTool

HTTP_TIMEOUT_TIME = 120  # http请求等待超时时间  （秒）
RETRY = 3
user = UserInfo()
flag401 = False


def addInfoToAllure(response, startTime, scene, isWriteBody=False):
    """
    添加请求响应信息到allure
    :param isWriteBody: 是否写入请求参数和返回结果
    :param scene: 请求账号
    :param startTime: 开始时间
    :param response: 请求响应数据
    :return:
    """
    pwd = user.getPassword(scene=scene)
    info = [
        f"startTime:  {startTime}",
        f"acc/pwd:  {scene}/{pwd}",
        f"endTime:  {date_time(days=0, fmt='%Y-%m-%d %H:%M:%S')}",
        f"s-trace-id:  {response.headers.get('s-trace-id')}",
        f"url:  {response.request.url}",
        f"method:  {response.request.method}",
        f"status_code:  {str(response.status_code)}",
        f"headers:  {str(str(response.request.headers))}"
    ]
    # print("\n\n".join(info))
    if isWriteBody:
        try:
            info.append("Response Body:\n" + json.dumps(response.json(), indent=4, ensure_ascii=False))
        except json.decoder.JSONDecodeError:
            info.append("Response Body:\n" + response.text)

        if response.request.body is not None:
            if isinstance(response.request.body, bytes):
                # 将json类型Post数据unicode转为中文字符串
                requestBody = response.request.body.decode('unicode-escape', errors="ignore")
                try:
                    info.append("Request Body:\n" + json.dumps(json.loads(requestBody), indent=4, ensure_ascii=False))
                except json.decoder.JSONDecodeError:
                    info.append("Request Body:\n" + requestBody)
            else:
                info.append("Request Body:\n" + response.request.body)

    allure.attach("\n\n".join(info), "Request&Response")


def returnUrl(path):
    if not path.startswith("http"):
        return baseinfo.protocol + "://" + baseinfo.secHost + baseinfo.host + baseinfo.port + path
    else:
        return path


def request(method, url, scene, **kwargs):
    """
    网络请求
    :param method: 方法
    :param url: 请求路径
    :param scene: 用户场景身份
    :param kwargs: 其他参数
    :return:
    """
    # 是否解析
    parseToJson = True
    if "parseToJson" in kwargs:
        parseToJson = kwargs.get("parseToJson")
        kwargs.pop("parseToJson")

    if "session" in user.sessionDict.keys():
        session = user.sessionDict.get("session")
    else:
        session = sessions.session()
        session.keep_alive = False
        retry = Retry(connect=RETRY, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        user.sessionDict["session"] = session

    # 获取headers
    headers = {"sec-fetch-site": "same-site"}
    if "headers" in kwargs:
        resHeaders = kwargs.get("headers")
        headers.update(resHeaders)
        kwargs.pop("headers")

    # 获取token
    token = user.getToken(scene=scene)
    if token is not None:
        headers.update(token)

    # 请求开始时间:
    startTime = date_time(days=0, fmt='%Y-%m-%d %H:%M:%S')

    try:
        url = returnUrl(url)
        res = session.request(method=method, url=returnUrl(url), headers=headers, cookies={"language": "zh_CN"}, timeout=HTTP_TIMEOUT_TIME, **kwargs)
    except requests.exceptions.ReadTimeout:
        allure.attach("\n\n".join([f"请求账号:\t{scene}", f"开始请求时间:\t{startTime}", f"请求URL:\t{returnUrl(url)}"]),  "RequestInfo")
        assert False, "请求超时了~~"

    if res.status_code == 500:
        with allure.step(f"*************请求{res.status_code}啦*************"):
            addInfoToAllure(res, startTime=startTime, scene=scene, isWriteBody=True)
            assert False, f"请求{res.status_code}啦, 快去处理吧~~~"
    else:
        # 添加请求和响应信息到allure
        addInfoToAllure(res, startTime=startTime, scene=scene, isWriteBody=True)

    # token失效重新登录
    if res.status_code== 401 and scene is not None and user.getPassword(scene) is not None:
        global flag401
        if flag401 is True:
            return
        # 解析
        try:
            # 重新登录
            loginUrl = f"/oauth/oauth/token?client_id=client&client_secret=secret&grant_type=password&username={scene}&password={user.getPassword(scene)}"
            res2 = session.request(method="post", url=returnUrl(loginUrl))
            loginDic = res2.json()
            token = loginDic.get("access_token")
            tokenType = loginDic.get("token_type")
            assert token is not None, "access_token 为空"
            assert tokenType is not None, "token_type 为空"
            headers = dict(Authorization=tokenType + " " + token)
            # 更新token
            UserInfo.updateAccToken(scene=scene, token=headers)

        except:
            assert False, "重新登录失败"

    def parseRes(res):
        try:
            dic: object = res.json()
            if isinstance(dic, dict) and dic.get("failed") is True:
                try:
                    with allure.step("*************请求报错接口*************"):
                        # 添加请求失败在报告中的标记
                        addInfoToAllure(res, startTime=startTime, scene=scene, isWriteBody=True)
                        assert False
                except:
                    pass
            return dic
        except :
            pass

    if parseToJson:
        return parseRes(res=res)
    else:
        parseRes(res=res)
        return res


def get(url, params=None, parseToJson=True, scene=None, **kwargs):
    return request('get', url, params=params, parseToJson=parseToJson, scene=scene, **kwargs)


def post(url, params=None, data=None, json=None, parseToJson=True, scene=None, **kwargs):
    return request('post', url, params=params, data=data, json=json, parseToJson=parseToJson, scene=scene, **kwargs)


def put(url, params=None, data=None, parseToJson=True, scene=None, **kwargs):
    return request('put', url, params=params, data=data, parseToJson=parseToJson, scene=scene, **kwargs)


def options(url, scene=None, **kwargs):
    return request('options', url, scene=scene, **kwargs)


def head(url, scene=None, **kwargs):
    return request('head', url, scene=scene, **kwargs)


def patch(url, data=None, scene=None, **kwargs):
    return request('patch', url, data=data, scene=scene, **kwargs)


def delete(url, parseToJson=True, scene=None, **kwargs):
    return request('delete', url, scene=scene, parseToJson=parseToJson, **kwargs)


def getDataWithSize(url, params, scene, size=100):
    """
    分页请求
    :param url: 请求path
    :param params: 请求参数
    :param scene: 请求账号
    :param size: 每次请求多少
    :return: 总共数据
    """
    dataList = []
    page = 0
    while True:
        params["page"] = page
        params["size"] = size
        res = get(url=url, scene=scene, params=params, parseToJson=False)
        if res.status_code != 200:
            return res
        else:
            try:
                dic = res.json()
                assert isinstance(dic, dict) and isinstance(dic.get("content"), list)
                dataList.extend(dic.get("content"))
                if dic['empty']:
                    break
                page += 1
            except:
                return res

    return dataList


def decrypt(parm):
    """
    系统中加密数据解密
    :param parm:
    :return:
    """
    # 1.0登录(因为是dev环境解密,所以使用dev环境账号登录获取token)
    url = f"/oauth/oauth/token?client_id=client&client_secret=secret&grant_type=password&username={UserInfo.accNumSourceParallelZTB.purAccNum}&password={UserInfo.password}"
    loginDic = post(url=url)
    token = loginDic.get("access_token")
    assert token is not None, "access_token 为空"
    headers = dict(Authorization=token)

    # 解密
    url = f"/hpfm/v1/srm/crypto/decrypt?encryptedStr={parm}"
    res = get(url=url, headers=headers)
    if isinstance(res, int):
        print(res)
        return res
    else:
        assert isinstance(res, dict), res
        code = res.get("code")
        assert code is not None
        codeList = res.get("code").split(sep=" ")
        assert len(codeList) > 0
        print(codeList[0])
        # 返回解密数据
        return codeList[0]


if __name__ == '__main__':
    # loginAll()
    decrypt("__-ABTulNBseknIACo0vOHBIg-__")
    # url = "https://test.isrm.going-link.com/oauth/oauth/token?client_id=AUTO&client_secret=hand1234&grant_type=password&username=18156781234&password=hand1234"
    # res = post(url=url)
    # print(res)
