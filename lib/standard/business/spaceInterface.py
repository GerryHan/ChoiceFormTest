# from config.globals import serverName
# from config.globals.userInfo import UserInfo
# from tools import request
#
# user = UserInfo()
# txapi = serverName.txapi
# tenant_id = "6385b14174a84547035e28ba"
# scene = "testing@choiceform.com"
#
#
# class SpaceInterface:
#
#     @staticmethod
#     def createSpace(name="创建空间", scene=scene):
#         """
#         :param name:
#         :param scene:
#         data = {
#         name: "测试空间1号"，
#         tenant_id: "6385b14174a84547035e28ba"
#         }
#         :return:
#         """
#         # 新建空间
#         url = f"{txapi}/workspaces"
#         data = {
#             "name": name,
#             "tenant_id": tenant_id
#         }
#         res = request.post(url=url, json=data, scene=scene, parseToJson=False)
#         assert res.status_code == 201, "创建空间失败"
#         return res
