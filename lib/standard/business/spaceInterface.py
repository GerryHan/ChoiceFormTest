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
#     def createSpace(name="�����ռ�", scene=scene):
#         """
#         :param name:
#         :param scene:
#         data = {
#         name: "���Կռ�1��"��
#         tenant_id: "6385b14174a84547035e28ba"
#         }
#         :return:
#         """
#         # �½��ռ�
#         url = f"{txapi}/workspaces"
#         data = {
#             "name": name,
#             "tenant_id": tenant_id
#         }
#         res = request.post(url=url, json=data, scene=scene, parseToJson=False)
#         assert res.status_code == 201, "�����ռ�ʧ��"
#         return res
