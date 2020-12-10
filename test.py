from AutoTest import AutoTest

class Test(AutoTest):
    def setUp(self) -> None:
        pass

    def test_execution(self):
        self.click_by_text("开发者选项")

    def tearDown(self) -> None:
        pass


