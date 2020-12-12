from AutoTest import AutoTest

class Test(AutoTest):

    def setUp(self):
        self.system_path = self.args.get("system_path")

    def test_a(self):
        self.click_list_text(self.system_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    t = Test()
    t.test_a()
