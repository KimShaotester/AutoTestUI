import unittest
import argparse
import json
import uiauto


class AutoTest(unittest.TestCase, uiauto):
    def __init__(self):
        super(AutoTest, self).__init__()
        self._parser = self.get_parser()
        self._dict = self.read_json_file()

        self.suite = self._dict.get("suitename")
        self.case = self._dict.get("casename")
        self.device = self._dict.get("ip")
        self.args = self._dict.get("parameters")
        self.job = self._dict.get("jobid")
        self.log = self._dict.get("log")

        # self.device_initialize()

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


class test(AutoTest):
    def setUp(self) -> None:
        self.ip = "192.168.81.108"
        self.device_initialize()

    def test_a(self):
        self.click_by_text("开发者选项")

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    t = test()
    t.test_a()
