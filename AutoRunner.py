import pymysql
import re
import os
import json
import datetime
import time
import threading

# class Key():
#     fetchone = "fetchone"
#     fetchall = "fetchall"
#
# class SqlTool():
#     def __init__(self):
#         self._db = self.connect()
#         self._cursor = self._db.cursor()
#
#     def connect(self):
#         return pymysql.connect("localhost", "root", "123456", "autotest")
#
#     def sql_run(self, sql):
#         return self._cursor.execute(sql)
#
#     def sql_filter(self, sql, filter=Key.fetchone):
#         self.sql_run(sql)
#         if filter == Key.fetchone:
#             return self._cursor.fetchone()
#         elif filter == Key.fetchall:
#             return self._cursor.fetchall()
#
#     def sql_commit(self,sql):
#         self.sql_run(sql)
#         self._db.commit()
#
#     def __del__(self):
#         self._cursor.close()
#         self._db.close()


db = pymysql.connect("localhost", "root", "123456", "autotest")
cursor = db.cursor()

def run_suite(suite):
    sql = "select suiteCase from suite where suiteName = '{}'".format(suite)
    cursor.execute(sql)
    data = cursor.fetchone()
    caseList = data[0].split(',')
    JobResult = "pass"
    starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    jobowner = "jinchao"

    # print (caseList)
    # print (starttime, type(starttime))
    # print (suite)
    # print (device)

    sql = "insert into result (suite, device, starTtime, jobOwner) " \
          "values ('{}', '{}', '{}', '{}')".format(suite, device, starttime, jobowner)
    cursor.execute(sql)
    db.commit()

    for case in caseList:
        sql = "select `key`, `value` from parameters where parameters.Case_id = " \
              "(select caseId from `case` where caseName = '{}')".format(case)

        cursor.execute(sql)
        data = cursor.fetchall()
        print (data)

        dict_parameters = {}
        for value in data:
            dict_parameters[value[0]] = value[1]

        user = os.path.expanduser('~')
        log = os.path.join(user, "AutoTest", str(jobid), suite, case)

        if not os.path.exists(log):
            os.makedirs(log)

        input_dict["parameters"] = dict_parameters
        input_dict["casename"] = case
        input_dict["log"] = log

        input_json = log + "\input.json"
        with open(input_json, "w+") as f:
            f.write(json.dumps(input_dict))

        sql = "select caseScripts from `case` where caseName='{}'".format(case)
        cursor.execute(sql)
        data = cursor.fetchone()
        script = data[0]
        os.system("python {} --input {}".format(script, input_json))

        result = log + "\\result.json"
        # result = "C:\\Users\\jinchao\\result.json"
        if os.path.exists(result):
            with open(result) as f:
                result_dict = json.loads(f.read())
                startTime = result_dict.get("startTime")
                endTime = result_dict.get("endTime")
                log = result_dict.get("log")
                result = result_dict.get("result")
        else:
            result = "fail"
            startTime = endTime = log = None

        if result == "fail":
            JobResult = "fail"

        print("{}\n{}\n{}\n{}\n{}\n".format(case, startTime, endTime, log, result))
        sql = "insert into caseResult (`case`, startTime, endTime, log, result)" \
              "values ( '{}', '{}', '{}', '{}', '{}')".format(case, startTime, endTime, log, result)
        cursor.execute(sql)
        db.commit()

    endTime = datetime.datetime.now()
    sql = "update result set endTime='{}', result='{}' where jobId = {}".format(endTime, JobResult, jobid)
    cursor.execute(sql)
    db.commit()

while True:
    sql = "SELECT COUNT(*) FROM execute"
    cursor.execute(sql)
    data = cursor.fetchone()

    for i in range(1, data[0]+1):
        print ("id is {}".format(i))
        sql = "select * from execute where id={}".format(i)
        cursor.execute(sql)
        data = cursor.fetchone()
        print (data)

        input_dict = {}
        if data[3] == 1:
            suite = data[1]
            device = data[2]

            # print (suite)

            sql = "SELECT MAX(jobId) FROM result"
            cursor.execute(sql)
            data = cursor.fetchone()
            jobid = data[0] + 1

            # print (jobid)

            input_dict["jobid"] = jobid
            input_dict["suite"] = suite
            input_dict["ip"] = device

            # run_suite(suite)
            thread = threading.Thread(target=run_suite, args=(suite,))
            thread.start()

        time.sleep(2)

