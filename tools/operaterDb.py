import time
import pymysql as mysql
from config.globals.environment import env, isConnectDB


class DBTool(object):
    countNum = 0
    db = None
    dbconfig = {
        "host": "10.2.100.85",
        "port": 3306,
        "user": "autoTest",
        "password": "123456",
        "charset": "utf8",
        "database": 'standard_monitoring'
    }

    @staticmethod
    def openDB():
        if DBTool.db is None:
            db = mysql.connect(**DBTool.dbconfig)
            DBTool.countNum += 1
            print(f"第 {DBTool.countNum} 次链接数据库")
        elif DBTool.db is not None and DBTool.db.open is not True:
            DBTool.countNum += 1
            print(f"第 {DBTool.countNum} 次链接数据库")
            db = mysql.connect(**DBTool.dbconfig)
        else:
            db = DBTool.db
        DBTool.db = db

    @staticmethod
    def closeDB():
        if DBTool.db is not None and DBTool.db.open is True:
            DBTool.db.close()

    @staticmethod
    def executeSql(sql, case_code, status):
        if isConnectDB is not True:
            return
        DBTool.openDB()
        assert DBTool.db.open, "请先打开数据库"

        if env == "test":
            updateStatus = f'update test_monitor set execute_status={status} WHERE case_code="{case_code}";'
            updateResult = f'update test_monitor set execute_result={status} WHERE case_code="{case_code}";'
        elif env == "prod":
            updateStatus = f'update prod_monitor set execute_status={status} WHERE case_code="{case_code}";'
            updateResult = f'update prod_monitor set execute_result={status} WHERE case_code="{case_code}";'
        # 执行数据
        cursor = DBTool.db.cursor()
        if sql == "updateStatus":
            sql = updateStatus
            cursor.execute(sql)
        elif sql == "updateResult":
            sql = updateResult
            cursor.execute(sql)

    @staticmethod
    def queryCode(waitTime):
        if isConnectDB is False:
            DBTool.openDB()
        assert DBTool.db.open, "请先打开数据库"
        sql = "SELECT * FROM ver_code"
        for i in range(waitTime):
            db = mysql.connect(**DBTool.dbconfig)
            DBTool.db = db
            cursor = DBTool.db.cursor()
            # 执行数据
            cursor.execute(sql)
            result = cursor.fetchall()
            resultList = [item for item in result if item is not None]
            if len(resultList) > 0:
                code = resultList[0][0]
                DBTool.deleteCode(code)
                DBTool.closeDB()
                return code
            else:
                time.sleep(1)
        else:
            assert False, "数据库中未查询到验证码"

    @staticmethod
    def deleteCode(code):
        sql = f"DELETE FROM ver_code WHERE ver_code={code}"
        db = mysql.connect(**DBTool.dbconfig)
        DBTool.db = db
        cursor = DBTool.db.cursor()
        # 执行数据
        cursor.execute(sql)
        # 提交数据库
        DBTool.db.commit()


    @staticmethod
    def insertEndTimeSql(suiteName):
        if isConnectDB is not True:
            return
        DBTool.openDB()
        assert DBTool.db.open, "请先打开数据库"
        # 插入数据
        cursor = DBTool.db.cursor()
        timeStamp = int(time.time())
        sql = f'UPDATE execute_time SET end_time={timeStamp} WHERE environment="{env}" AND suite_name="{suiteName}"'
        # 更新完成时间
        cursor.execute(sql)
        # 提交数据库
        DBTool.db.commit()

    @staticmethod
    def executeInsertSql(data):
        if isConnectDB is not True:
            return
        DBTool.openDB()
        assert DBTool.db.open, "请先打开数据库"
        # 插入数据
        cursor = DBTool.db.cursor()

        if env == "test":
            sql1 = "INSERT INTO test_monitor (suit_name,module_name,function_name,case_tags,case_sap,case_code,execute_status,execute_result) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        elif env == "prod":
            sql1 = "INSERT INTO prod_monitor (suit_name,module_name,function_name,case_tags,case_sap,case_code,execute_status,execute_result) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"

        # 插入时间
        for item in data:
            if item["case_sap"] == "sap":
                break
        else:
            timeStamp = int(time.time())
            suit_name = "".join(list(set([item["suit_name"] for item in data])))
            # 清除数据
            deleteSql = f"DELETE FROM execute_time WHERE environment= '{env}' and suite_name = '{suit_name}'"
            cursor.execute(deleteSql)
            # 插入数据
            values = (env, suit_name, timeStamp)
            sql = f"INSERT INTO execute_time (environment,suite_name,start_time) VALUES (%s,%s,%s)"
            cursor.execute(sql, values)


        # 插入数据
        for dic in data:
            values = (dic.get("suit_name"), dic.get("module_name"), dic.get("function_name"), dic.get("case_tags"), dic.get("case_sap"), dic.get("case_code"), "0", "0")
            try:
                cursor.execute(sql1, values)
            except:
                print("用例编号: {} 插入重复".format(dic.get("case_code")))

        # 提交数据库
        DBTool.db.commit()

    @staticmethod
    def collectUrl(url, method, kwargs=None):
        if isConnectDB is not True:
            return
        DBTool.openDB()
        assert DBTool.db.open, "请先打开数据库"
        # 查询是否重复
        db = mysql.connect(**DBTool.dbconfig)
        DBTool.db = db
        cursor = DBTool.db.cursor()
        if kwargs is not None:
            sql = f"SELECT * FROM collect_url where url='{url}' and method='{method}' and kwargs='{kwargs}';"
        else:
            sql = f"SELECT * FROM collect_url where url='{url}' and method='{method}' and kwargs is null;"
        # 执行数据
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            values = (url, kwargs, method)
            sql = f"INSERT INTO collect_url (url,kwargs,method) VALUES (%s,%s,%s)"
            cursor.execute(sql, values)
            # 提交数据库
            DBTool.db.commit()


def updateStatusToProcess(caseCode):
    DBTool.executeSql(sql="updateStatus", case_code=caseCode, status=1)


def updateResultToPass(caseCode):
    DBTool.executeSql(sql="updateResult", case_code=caseCode, status=2)


def updateResultToFailed(caseCode):
    DBTool.executeSql(sql="updateResult", case_code=caseCode, status=1)


def updateStatusToCompleted(caseCode):
    DBTool.executeSql(sql="updateStatus", case_code=caseCode, status=2)


def queryVerCode(waitTime=60):
    code = DBTool.queryCode(waitTime=waitTime)
    return code


if __name__ == '__main__':
    DBTool.queryCode(waitTime=60)



# if __name__ == '__main__':
    # executeSql(sql="updateResult", case_code="SRM-LOGIN-001", status=0)
    # updateResultToPass("SRM-LOGIN-001")
    # updateResultToFailed("SRM-LOGIN-001")
    # DBTool.insertEndTimeSql(suiteName="寻源套件")
    # ...
