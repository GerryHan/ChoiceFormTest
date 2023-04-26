# -*- coding = utf-8 -*-
# @Time: 2023/2/22 17:52
# @Author: Gerry
# @File: userInfo.py
# @Software: PyCharm
from config.globals import baseinfo as base
from tools.singLeton import Singleton
import copy


class AccountInfo:
    """
    账户信息
    """

    def __init__(self, token=None, accountNum=None, password=None, mockToken=None):
        super().__init__()

        # 密码
        self.password = password

        # 账号
        self.accountNum = accountNum

        # token信息
        self.token = token

        # mockToken信息
        self.mockToken = mockToken

        # 用户名称
        self.realName = None

        # 用户邮箱
        self.email = None

    def setAttrValue(self, info):
        """
        给属性赋值
        :param info:
        :return:
        """
        # 用户名称
        self.realName = info.get("realName")

        # 用户邮箱
        self.email = info.get("email")

    def updateToken(self, token):
        """
        更新token
        :param token:
        :return:
        """
        self.token = token

    def updateMockToken(self, token):
        """
        更新mockToken
        @param token:
        @return:
        """
        self.mockToken = token

    def setCompanyInfo(self, info):
        """
        给属性赋值
        :param info:
        :return:
        """
        # 公司名称
        self.companyName = info.get("companyName")

        # 公司名称
        self.companyNum = info.get("companyNum")


class GroupInfo(object):
    """
    账户组信息
    """

    accInfoDict = {}
    partnersDict = {}
    passwordDict = {}

    def __init__(self, accNumDict):
        super().__init__()
        assert accNumDict.get("groupName") is not None, f"账号未分组"
        self.groupName = accNumDict.get("groupName")
        if accNumDict.get("admin") is not None:
            self.admin = accNumDict.get("admin")
        if accNumDict.get("purAccNum") is not None:
            self.purAccNum = accNumDict.get("purAccNum")
        dic = copy.deepcopy(accNumDict)
        self.accNumDict = dic


class UserInfo(Singleton):
    # 所有账户密码
    password = "cftesting"
    # 协同非并发0组
    dev1 = GroupInfo(base.dev1)
    sessionDict = {}

    __count = 0

    def __init__(self):
        super().__init__()

        if UserInfo.__count >= 1:
            return
        UserInfo.__count += 1

    @staticmethod
    def setAccToken(scene, token, password):
        """
        创建账户对象并设置token
        :param password: 密码
        :param scene: 场景
        :param token:
        :return:
        """
        if GroupInfo.accInfoDict.get(scene) is not None:
            account: AccountInfo = GroupInfo.accInfoDict.get(scene)
            account.updateToken(token=token)
        else:
            GroupInfo.accInfoDict[scene] = AccountInfo(token=token, accountNum=scene, password=password)
            print(GroupInfo.accInfoDict[scene])

    @staticmethod
    def setMockToken(mockToken, scene):
        """
        创建账户对象并设置mockToken
        @param mockToken:
        @param scene:
        @return:
        """
        if GroupInfo.accInfoDict.get(scene) is not None:
            account: AccountInfo = GroupInfo.accInfoDict.get(scene)
            account.updateMockToken(token=mockToken)
        else:
            GroupInfo.accInfoDict[scene] = AccountInfo(mockToken=mockToken)

    @staticmethod
    def updateAccToken(scene, token):
        """
        更新token
        :param scene: 场景
        :param token:
        :return:
        """
        if GroupInfo.accInfoDict.get(scene) is not None:
            accInfo: AccountInfo = GroupInfo.accInfoDict.get(scene)
            accInfo.updateToken(token=token)

    @staticmethod
    def getToken(scene):
        """
        获取token
        :param scene:
        :return:
        """
        if GroupInfo.accInfoDict.get(scene) is not None:
            accInfo: AccountInfo = GroupInfo.accInfoDict.get(scene)
            return accInfo.token
        else:
            return None

    @staticmethod
    def getMockToken(scene):
        """
        获取token
        :return:
        """
        if GroupInfo.accInfoDict.get(scene) is not None:
            accInfo: AccountInfo = GroupInfo.accInfoDict.get(scene)
            return accInfo.mockToken
        else:
            return None

    @staticmethod
    def getPassword(scene):
        """
        获取password
        :param scene:
        :return:
        """
        if GroupInfo.accInfoDict.get(scene) is not None:
            accInfo: AccountInfo = GroupInfo.accInfoDict.get(scene)
            return accInfo.password
        # else:
        #     return ""
