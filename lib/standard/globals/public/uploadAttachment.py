# -*- coding = utf-8 -*-
# @Time: 2023/2/2 10:13
# @Author: Gerry
# @File: uploadAttachment.py
# @Software: PyCharm

from globalImportBase import UserInfo, request, serverName
user = UserInfo()

def uploadAttachment(uploadUrl, filePath, data, scene=""):
    """
    上传附件
    :param filePath: 本地文件路径
    :param scene: 场景类型
    :param uploadUrl: 上传服务器路径
    :param data: 数据
    :return: 返回文件地址
    data 结构
    bucketName: private-bucket
    directory: spfm-comp
    file: (binary)
    """
    # 把目标文件以open打开，然后存储到变量upfile里面存到一个字典里，注意这里的upfile不是随便起的，要看后台的接收数据的时候，使用的接收文件信息的key是如何定义的。一定要按照服务端的key来
    getFileName = filePath.split("/")
    assert len(getFileName) > 0 and "." in getFileName[-1]
    getFileType = getFileName[-1].split(".")
    assert len(getFileType) == 2
    fileType = getFileType[1]
    value = (getFileName[-1], open(filePath, 'rb'))
    if fileType == "docx":
        value = value + ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",)
    elif fileType == "doc":
        value = value + ("application/msword",)
    elif fileType == "pdf":
        value = value + ("application/pdf",)
    elif fileType == "jpg":
        value = value + ("image/jpeg",)
    elif fileType == "txt":
        value = value + ("text/plain",)
    elif fileType == "png":
        value = value + ("image/png",)
    elif fileType == "xlsx":
        value = value + ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",)
    files = {'file': value}
    res = request.post(url=uploadUrl, data=data, files=files, scene=scene, parseToJson=False)
    return res


def uploadExcelAttachment(uploadUrl, fileName, dataPath, data=None, parseToJson=False, scene=""):
    """
    上传excel附件
    :param scene: 场景类型
    :param uploadUrl: 上传服务器路径
    :param fileName: 文件名称
    :param dataPath: 文件路径
    :param data: 上传excel文件额外参数
    :return: 返回文件地址
    files结构
    e.g：files = {'name': (fileName, open(filePath, 'rb'), 'Content-Type')}
    若接口需多传param，则需传data,格式为：
    param = {
                "key": json.dumps(value)
            }
    data = {
        "param": json.dumps(param)
    }
    """
    files = {
        'excel': (fileName, open(dataPath, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    }
    return request.post(url=uploadUrl, files=files, data=data, scene=scene, parseToJson=parseToJson)


def uploadExcel(uploadUrl, fileName, dataPath, data=None, parseToJson=False, scene=""):
    """
    上传excel附件
    :param scene: 场景类型
    :param uploadUrl: 上传服务器路径
    :param fileName: 文件名称
    :param dataPath: 文件路径
    :param data: 上传excel文件额外参数
    :return: 返回文件地址
    files结构
    e.g：files = {'name': (fileName, open(filePath, 'rb'), 'Content-Type')}
    若接口需多传param，则需传data,格式为：
    param = {
                "key": json.dumps(value)
            }
    data = {
        "param": json.dumps(param)
    }
    """
    files = {
        'file': (fileName, open(dataPath, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    }
    return request.post(url=uploadUrl, files=files, data=data, scene=scene, parseToJson=parseToJson)


def deleteAttachment(attachmentUUID, bucketName, data, scene=""):
    """
    删除附件
    :param bucketName:
    :param attachmentUUID: 附件ID
    :param scene: 场景类型
    :param data: 参数
    :return:
    """
    choice = user.getTenantId(scene=scene)
    url = f"{serverName.hfle}{tid}/files/delete-by-uuidurl?attachmentUUID={attachmentUUID}&bucketName={bucketName}"
    return request.post(url=url, json=data, scene=scene)


def queryFilesuuid(tenantId=None, scene=""):
    """
    查询 附件的UUID
    :return:
    """
    if tenantId is not None:
        return request.post(url=f"{serverName.hfle}files/uuid?tenantId={tenantId}", scene=scene)
    else:
        return request.post(url=f"{serverName.hfle}files/uuid?", scene=scene)


def queryAttachment(attachmentUUID, bucketName="private-bucket", directory="", scene=""):
    """
    查询附件
    :param directory: 目录
    :param scene: 场景类型
    :param bucketName:
    :param attachmentUUID:
    :return:
    """
    return request.get(url=f"{serverName.hfle}files/{attachmentUUID}/file?attachmentUUID={attachmentUUID}&bucketName={bucketName}&directory={directory}", scene=scene)


def queryAttachByUuid(attachmentUUID, bucketName, scene=""):
    tid = user.getTenantId(scene=scene)
    url = f"{serverName.hfle}{tid}/files/{attachmentUUID}/file?attachmentUUID={attachmentUUID}&bucketName={bucketName}&tenantId={tid}"
    response = request.get(url=url, scene=scene)
    assert isinstance(response, list), response
    return response

