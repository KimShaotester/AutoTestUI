from AutoTest import AutoTest

class Test(AutoTest):

    def setUp(self):
        pass

    def test_a(self):
        self.click_by_text("开发者选项")

    def tearDown(self):
        pass

if __name__ == '__main__':
    t = Test()
    t.test_a()


