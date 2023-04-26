from tools import request
import re
import allure
from tools.rsaTool import encrypt
from config.globals.userInfo import UserInfo
from lib.standard.globals.public.userSelf import userSelf

user = UserInfo()


def regSearchString(StringOrg, StingReg):
    pattern = re.compile(StingReg)
    search = pattern.search(StringOrg)
    if search:
        return search.group(0)
    else:
        return "返回HTML页面中未找到【登录失败】提示信息"


def login(username, password, scene=UserInfo.platform, ass=""):
    # 如果登录账号不是默认设置的,提示
    assert username == scene, "请用场景默认账号登录"

    # 登录主接口，输入登录参数
    data = {"username": username, "password": encrypt(password)}
    r_login = request.post("/oauth/", data=data, allow_redirects=False, parseToJson=False, scene=scene)
    cookie = r_login.headers.get('Set-Cookie')
    redirect_url = r_login.headers.get('location')
    # 判断登录参数，正确参数流程
    # if cookie is not None and 'type=account' not in redirect_url:
    if cookie is not None:
        authorization = request.get(f"/oauth/oauth/authorize?response_type=token&client_id=srm-portal&redirect_uri={redirect_url}/?hasLogin=true", allow_redirects=False, parseToJson=False, scene=scene)
        # access_token = "bearer " + re.search("access_token=(.*?)&", authorization.headers["location"]).group(1)
        assert authorization.headers.get("location") is not None, "location 为空"
        assert re.search("access_token=(.*?)&", authorization.headers.get("location")) is not None
        access_token = "bearer " + re.search("access_token=(.*?)&", authorization.headers.get("location")).group(1)
        assert ass in access_token
        allure.attach(access_token, "access_token")

        # 登录后数据存储到公共文件
        headers = dict(Authorization=access_token)
        user.tokenDict[scene] = headers
        # 获取用户信息
        userSelf(scene=scene)
        return headers

    # 判断登录参数，错误参数流程
    elif 'type=account' in redirect_url:
        accountTip = request.get("/oauth/?type=account", allow_redirects=False, parseToJson=False)
        response = accountTip.content.decode('utf-8')
        regular = r'<label class="validation errmsg">(.*?)</label>'
        ret = regSearchString(StringOrg=response, StingReg=regular)
        assert ass in ret

# if __name__ == '__main__':
# print(login("18123456789", "hand1234"))
# print(get_user_info(login("18110000010", "hand1234")))
# print(login(baseinfo.username, baseinfo.password))

# print(get_user_info())
