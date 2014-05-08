import unittest
from sahi import Browser, Element


class TC_MyTest(unittest.TestCase):
    def test_to_s_single(self):
        self.assertEqual("_sahi._div(\"id\")", str(Element(None, "div", ["id"])))
        self.assertEqual("_sahi._lastAlert()",  str(Element(None, "lastAlert", [])))

    def test_to_s_multi_strings(self):
        self.assertEqual("_sahi._div(\"id\", \"id2\")", str(Element(None, "div", ["id", "id2"])))

    def test_to_s_multi_stubs(self):
        stub2 = Element(None, "div", ["id2"])
        near = Element(None, "near", [stub2])
        stub1 = Element(None, "div", ["id1", near])
        self.assertEqual("_sahi._div(\"id1\", _sahi._near(_sahi._div(\"id2\")))", str(stub1))

    def test_browser_multi_stubs(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._div(\"id\")", str(browser.div("id")))
        self.assertEqual("_sahi._div(\"id\", \"id2\")", str(browser.div("id", "id2")))
        self.assertEqual("_sahi._div(\"id1\", _sahi._near(_sahi._div(\"id2\")))", str(browser.div("id1").near(browser.div("id2"))))

    def test_xy(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._xy(_sahi._div(\"id\"), 10, 20)", str(browser.div("id").xy(10, 20)))

    def test_under_no_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._under(_sahi._cell(\"Heading\")))", str(browser.cell(0).under(browser.cell("Heading"))))

    def test_right_of_no_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._rightOf(_sahi._cell(\"Heading\")))", str(browser.cell(0).right_of(browser.cell("Heading"))))

    def test_left_of_no_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._leftOf(_sahi._cell(\"Heading\")))", str(browser.cell(0).left_of(browser.cell("Heading"))))

    def test_left_or_right_of_no_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._leftOrRightOf(_sahi._cell(\"Heading\")))", str(browser.cell(0).left_or_right_of(browser.cell("Heading"))))

    def test_above_no_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._above(_sahi._cell(\"Heading\")))", str(browser.cell(0).above(browser.cell("Heading"))))

    def test_above_or_under_no_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._aboveOrUnder(_sahi._cell(\"Heading\")))", str(browser.cell(0).above_or_under(browser.cell("Heading"))))

    def test_above_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._above(_sahi._cell(\"Heading\"), [10,5], 20))", str(browser.cell(0).above(browser.cell("Heading"), [10, 5], 20)))
        self.assertEqual("_sahi._cell(0, _sahi._above(_sahi._cell(\"Heading\"), 10, 20))", str(browser.cell(0).above(browser.cell("Heading"), 10, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._above(_sahi._cell(\"Heading\"), 10, null))", str(browser.cell(0).above(browser.cell("Heading"), 10)))
        self.assertEqual("_sahi._cell(0, _sahi._above(_sahi._cell(\"Heading\"), null, 20))", str(browser.cell(0).above(browser.cell("Heading"), None, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._above(_sahi._cell(\"Heading\")))", str(browser.cell(0).above(browser.cell("Heading"), None, None)))

    def test_above_or_under_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._aboveOrUnder(_sahi._cell(\"Heading\"), [10,5], 20))", str(browser.cell(0).above_or_under(browser.cell("Heading"), [10, 5], 20)))
        self.assertEqual("_sahi._cell(0, _sahi._aboveOrUnder(_sahi._cell(\"Heading\"), 10, 20))", str(browser.cell(0).above_or_under(browser.cell("Heading"), 10, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._aboveOrUnder(_sahi._cell(\"Heading\"), 10, null))", str(browser.cell(0).above_or_under(browser.cell("Heading"), 10)))
        self.assertEqual("_sahi._cell(0, _sahi._aboveOrUnder(_sahi._cell(\"Heading\"), null, 20))", str(browser.cell(0).above_or_under(browser.cell("Heading"), None, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._aboveOrUnder(_sahi._cell(\"Heading\")))", str(browser.cell(0).above_or_under(browser.cell("Heading"), None, None)))

    def test_under_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._under(_sahi._cell(\"Heading\"), [10,5], 20))", str(browser.cell(0).under(browser.cell("Heading"), [10, 5], 20)))
        self.assertEqual("_sahi._cell(0, _sahi._under(_sahi._cell(\"Heading\"), 10, 20))", str(browser.cell(0).under(browser.cell("Heading"), 10, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._under(_sahi._cell(\"Heading\"), 10, null))", str(browser.cell(0).under(browser.cell("Heading"), 10)))
        self.assertEqual("_sahi._cell(0, _sahi._under(_sahi._cell(\"Heading\"), null, 20))", str(browser.cell(0).under(browser.cell("Heading"), None, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._under(_sahi._cell(\"Heading\")))", str(browser.cell(0).under(browser.cell("Heading"), None, None)))

    def test_left_of_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._leftOf(_sahi._cell(\"Heading\"), [10,5], 20))", str(browser.cell(0).left_of(browser.cell("Heading"), [10,5], 20)))
        self.assertEqual("_sahi._cell(0, _sahi._leftOf(_sahi._cell(\"Heading\"), 10, 20))", str(browser.cell(0).left_of(browser.cell("Heading"), 10, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._leftOf(_sahi._cell(\"Heading\"), 10, null))", str(browser.cell(0).left_of(browser.cell("Heading"), 10)))
        self.assertEqual("_sahi._cell(0, _sahi._leftOf(_sahi._cell(\"Heading\"), null, 20))", str(browser.cell(0).left_of(browser.cell("Heading"), None, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._leftOf(_sahi._cell(\"Heading\")))", str(browser.cell(0).left_of(browser.cell("Heading"), None, None)))

    def test_right_of_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._rightOf(_sahi._cell(\"Heading\"), [10,5], 20))", str(browser.cell(0).right_of(browser.cell("Heading"), [10,5], 20)))
        self.assertEqual("_sahi._cell(0, _sahi._rightOf(_sahi._cell(\"Heading\"), 10, 20))", str(browser.cell(0).right_of(browser.cell("Heading"), 10, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._rightOf(_sahi._cell(\"Heading\"), 10, null))", str(browser.cell(0).right_of(browser.cell("Heading"), 10)))
        self.assertEqual("_sahi._cell(0, _sahi._rightOf(_sahi._cell(\"Heading\"), null, 20))", str(browser.cell(0).right_of(browser.cell("Heading"), None, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._rightOf(_sahi._cell(\"Heading\")))", str(browser.cell(0).right_of(browser.cell("Heading"), None, None)))

    def test_left_or_right_of_extra_params(self):
        browser = Browser("", "", "")
        self.assertEqual("_sahi._cell(0, _sahi._leftOrRightOf(_sahi._cell(\"Heading\"), [10,5], 20))", str(browser.cell(0).left_or_right_of(browser.cell("Heading"), [10,5], 20)))
        self.assertEqual("_sahi._cell(0, _sahi._leftOrRightOf(_sahi._cell(\"Heading\"), 10, 20))", str(browser.cell(0).left_or_right_of(browser.cell("Heading"), 10, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._leftOrRightOf(_sahi._cell(\"Heading\"), 10, null))", str(browser.cell(0).left_or_right_of(browser.cell("Heading"), 10)))
        self.assertEqual("_sahi._cell(0, _sahi._leftOrRightOf(_sahi._cell(\"Heading\"), null, 20))", str(browser.cell(0).left_or_right_of(browser.cell("Heading"), None, 20)))
        self.assertEqual("_sahi._cell(0, _sahi._leftOrRightOf(_sahi._cell(\"Heading\")))", str(browser.cell(0).left_or_right_of(browser.cell("Heading"), None, None)))

if __name__ == '__main__':
    unittest.main()
