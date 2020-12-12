import datetime
import argparse
import json
from uiauto import uiauto

def run_clock(func):
    def execution():
        start = datetime.datetime.now()
        func()
        end = datetime.datetime.now()
        return (start, end)
    return execution()

class AutoTest(uiauto):
    def __init__(self):
        super(AutoTest, self).__init__()
        self._parser = self.get_parser()
        self._dict = self.read_json_file()

        self.suite = self._dict.get("suitename")
        self.case = self._dict.get("casename")
        self.ip = self._dict.get("ip")
        self.args = self._dict.get("parameters")
        self.job = self._dict.get("jobid")
        self.log = self._dict.get("log")
        self.start = datetime.datetime.now()

        self.device_initialize()

    def get_parser(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-i", "--input", dest='input', help="input json config for case")
        return self.parser.parse_args()

    def read_json_file(self):
        file = self._parser.input
        with open(file, "r+") as f:
            return json.loads(f.read())

    def set_result(self, result, comments=""):
        result = self.log + '\\result.json'

        dict = {}
        if result:
            dict["result"] = "pass"
        if comments:
            dict["comments"] = comments

        with open(result) as f:
            f.write(json.dumps(dict))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @run_clock
    def execute(self):
        pass


# import datetime
# def run_clock(func):
#     def execution(*args, **kwargs):
#         start = datetime.datetime.now()
#         func()
#         end = datetime.datetime.now()
#         kwargs["start"] = start
#         kwargs["end"] = end
#     return execution
#
# import time
# @run_clock
# def test(*args, **kwargs):
#     print ("aaaaa")
#     time.sleep(5)
#     print ("bbbbb")
#     print (kwargs["end"])
#
# a = test()
# print (a)

