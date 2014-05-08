import time
import unittest
from sahi import Browser, Element


class SahiDriverTest(unittest.TestCase):
    def setUp(self):
        self.browser_name = "firefox"
        self.browser = Browser(self.browser_name)
        self.browser.open()
        self.base_url = "http://sahi.co.in"

    def tearDown(self):
        self.browser.set_speed = 100
        self.browser.close()
        time.sleep(1)

    def test1(self):
        self.browser.navigate_to(self.base_url + "/demo/formTest.htm")
        self.browser.textbox("t1").value = "aaa"
        self.browser.link("Back").click()
        self.browser.link("Table Test").click()
        print(self.browser.cell("CellWithId"))
        print(self.browser.cell("CellWithId").text)
        self.assertEqual("Cell with id", self.browser.cell("CellWithId").text)

    def xtest_ZK(self):
        self.browser.speed = 200
        self.browser.navigate_to("http://www.zkoss.org/zkdemo/userguide/")
        self.browser.div("Hello World").click()
        self.browser.span("Pure Java").click()
        self.browser.div("Various Form").click()
        ## self.browser.wait(5000) {self.browser.textbox("z-intbox[1]").is_visible()}

        self.browser.div("Comboboxes").click()
        self.browser.textbox("z-combobox-inp").value = "aa"
        self.browser.italic("z-combobox-btn").click()
        self.browser.cell("Simple and Rich").click()

        self.browser.italic("z-combobox-btn[1]").click()
        self.browser.span("The coolest technology").click()
        self.browser.italic("z-combobox-btn[2]").click()
        self.browser.image("CogwheelEye-32x32.gif").click()
        self.assertTrue(self.browser.textbox("z-combobox-inp[2]").exists())

    def test_fetch(self):
        self.browser.navigate_to(self.base_url + "/demo/formTest.htm")
        self.assertEqual(self.base_url + "/demo/formTest.htm", self.browser.fetch("window.location.href"))

    def test_accessors(self):
        self.browser.navigate_to(self.base_url  + "/demo/formTest.htm")
        self.assertEqual("", self.browser.textbox("t1").value)
        self.assertTrue(self.browser.textbox(1).exists())
        self.assertTrue(self.browser.textbox("$a_dollar").exists())
        self.browser.textbox("$a_dollar").value = ("adas")
        self.assertEqual("", self.browser.textbox(1).value)
        self.assertTrue(self.browser.textarea("ta1").exists())
        self.assertEqual("", self.browser.textarea("ta1").value)
        self.assertTrue(self.browser.textarea(1).exists())
        self.assertEqual("", self.browser.textarea(1).value)
        self.assertTrue(self.browser.checkbox("c1").exists())
        self.assertEqual("cv1", self.browser.checkbox("c1").value)
        self.assertTrue(self.browser.checkbox(1).exists())
        self.assertEqual("cv2", self.browser.checkbox(1).value)
        self.assertTrue(self.browser.checkbox("c1[1]").exists())
        self.assertEqual("cv3", self.browser.checkbox("c1[1]").value)
        self.assertTrue(self.browser.checkbox(3).exists())
        self.assertEqual("", self.browser.checkbox(3).value)
        self.assertTrue(self.browser.radio("r1").exists())
        self.assertEqual("rv1", self.browser.radio("r1").value)
        self.assertTrue(self.browser.password("p1").exists())
        self.assertEqual("", self.browser.password("p1").value)
        self.assertTrue(self.browser.password(1).exists())
        self.assertEqual("", self.browser.password(1).value)
        self.assertTrue(self.browser.select("s1").exists())
        self.assertEqual("o1", self.browser.select("s1").selected_text())
        self.assertTrue(self.browser.select("s1Id[1]").exists())
        self.assertEqual("o1", self.browser.select("s1Id[1]").selected_text())
        self.assertTrue(self.browser.select(2).exists())
        self.assertEqual("o1", self.browser.select(2).selected_text())
        self.assertTrue(self.browser.button("button value").exists())
        self.assertTrue(self.browser.button("btnName[1]").exists())
        self.assertTrue(self.browser.button("btnId[2]").exists())
        self.assertTrue(self.browser.button(3).exists())
        self.assertTrue(self.browser.submit("Add").exists())
        self.assertTrue(self.browser.submit("submitBtnName[1]").exists())
        self.assertTrue(self.browser.submit("submitBtnId[2]").exists())
        self.assertTrue(self.browser.submit(3).exists())
        self.assertTrue(self.browser.image("imageAlt1").exists())
        self.assertTrue(self.browser.image("imageId1[1]").exists())
        self.assertTrue(self.browser.image(2).exists())
        self.assertFalse(self.browser.link("Back22").exists())
        self.assertTrue(self.browser.link("Back").exists())
        self.assertTrue(self.browser.accessor("document.getElementById('s1Id')").exists())

    def test_select(self):
        self.browser.navigate_to(self.base_url  + "/demo/formTest.htm")
        self.assertEqual("o1", self.browser.select("s1Id[1]").selected_text())
        self.browser.select("s1Id[1]").choose("o2")
        self.assertEqual("o2", self.browser.select("s1Id[1]").selected_text())
        self.browser.select(3).choose(["o1", "o3"])
        self.assertEqual("o1,o3", self.browser.select(3).selected_text())

    def test_set_file(self):
        self.browser.navigate_to(self.base_url  + "/demo/php/fileUpload.htm")
        self.browser.file("file").file("scripts/demo/uploadme.txt")
        self.browser.submit("Submit Single").click()
        self.assertTrue(self.browser.span("size").exists())
        self.assertIn("0.3046875 Kb", self.browser.span("size").text)
        self.assertIn("Single", self.browser.span("type").text)
        self.browser.link("Back to form").click()

    def test_multi_file_upload(self):
        self.browser.navigate_to(self.base_url  + "/demo/php/fileUpload.htm")
        self.browser.file("file[]").file("scripts/demo/uploadme.txt")
        self.browser.file("file[]").file("scripts/demo/uploadme2.txt")
        self.browser.submit("Submit Array").click()
        self.assertIn("Array", self.browser.span("type").text)
        self.assertIn("uploadme.txt", self.browser.span("file").text)
        self.assertIn("0.3046875 Kb", self.browser.span("size").text)

        self.assertIn("uploadme2.txt", self.browser.span("file[1]").text)
        self.assertIn("0.32421875 Kb", self.browser.span("size[1]").text)

    def test_clicks(self):
        self.browser.navigate_to(self.base_url  + "/demo/formTest.htm")
        self.assertIsNotNone(self.browser.checkbox("c1"))
        self.browser.checkbox("c1").click()
        self.assertEqual("true", self.browser.checkbox("c1").fetch("checked"))
        self.browser.checkbox("c1").click()
        self.assertEqual("false", self.browser.checkbox("c1").fetch("checked"))

        self.assertIsNotNone(self.browser.radio("r1"))
        self.browser.radio("r1").click()
        self.assertEqual("true", self.browser.radio("r1").fetch("checked"))
        self.assertTrue(self.browser.radio("r1").is_checked)
        self.assertFalse(self.browser.radio("r1[1]").is_checked)
        self.browser.radio("r1[1]").click()
        self.assertEqual("false", self.browser.radio("r1").fetch("checked"))
        self.assertTrue(self.browser.radio("r1[1]").is_checked)
        self.assertFalse(self.browser.radio("r1").is_checked)

    def test_links(self):
        self.browser.navigate_to(self.base_url  + "/demo/index.htm")
        self.browser.link("Link Test").click()
        self.browser.link("linkByContent").click()
        self.browser.link("Back").click()
        self.browser.link("link with return true").click()
        self.assertTrue(self.browser.textarea("ta1").exists())
        self.assertEqual("", self.browser.textarea("ta1").value)
        self.browser.link("Back").click()
        self.browser.link("Link Test").click()
        self.browser.link("link with return false").click()
        self.assertTrue(self.browser.textbox("t1").exists())
        self.assertEqual("formTest link with return false", self.browser.textbox("t1").value)
        self.assertTrue(self.browser.link("linkByContent").exists())

        self.browser.link("link with returnValue=false").click()
        self.assertTrue(self.browser.textbox("t1").exists())
        self.assertEqual("formTest link with returnValue=false", self.browser.textbox("t1").value)
        self.browser.link("added handler using js").click()
        self.assertTrue(self.browser.textbox("t1").exists())
        self.assertEqual("myFn called", self.browser.textbox("t1").value)
        self.browser.textbox("t1").value = ("")
        self.browser.image("imgWithLink").click()
        self.browser.link("Link Test").click()
        self.browser.image("imgWithLinkNoClick").click()
        self.assertTrue(self.browser.textbox("t1").exists())
        self.assertEqual("myFn called", self.browser.textbox("t1").value)
        self.browser.link("Back").click()

    def test_popup_title_name_mix(self):
        self.browser.navigate_to(self.base_url  + "/demo/index.htm")
        self.browser.link("Window Open Test").click()
        self.browser.link("Window Open Test With Title").click()
        self.browser.link("Table Test").click()

        popup_popwin = self.browser.popup("popWin")

        popup_popwin.link("Link Test").click()
        self.browser.link("Back").click()

        popup_with_title = self.browser.popup("With Title")

        popup_with_title.link("Form Test").click()
        self.browser.link("Table Test").click()
        popup_with_title.textbox("t1").value = ("d")
        self.browser.link("Back").click()
        popup_with_title.textbox(1).value = ("e")
        self.browser.link("Table Test").click()
        popup_with_title.textbox("name").value = ("f")
        self.assertIsNotNone(popup_popwin.link("linkByHtml").exists())

        self.assertIsNotNone(self.browser.cell("CellWithId"))
        self.assertEqual("Cell with id", self.browser.cell("CellWithId").text)
        popup_with_title.link("Break Frames").click()

        popupSahiTests = self.browser.popup("Sahi Tests")
        popupSahiTests.close()

        popup_popwin.link("Break Frames").click()
        popup_popwin.close()
        self.browser.link("Back").click()

    def test_in(self):
        self.browser.navigate_to(self.base_url  + "/demo/tableTest.htm")
        self.assertEqual("111", self.browser.textarea("ta").near(self.browser.cell("a1")).value)
        self.assertEqual("222", self.browser.textarea("ta").near(self.browser.cell("a2")).value)
        self.assertEqual("3", self.browser.table(0).fetch("rows.length"))
        self.browser.link("Go back").in_(self.browser.cell("a1").parent_node()).click()
        self.assertTrue(self.browser.link("Link Test").exists())

    def test_under(self):
        self.browser.navigate_to(self.base_url  + "/demo/tableTest.htm")
        self.assertEqual("x1-2", self.browser.cell(0).near(self.browser.cell("x1-0")).under(self.browser.tableHeader("header 3")).text)
        self.assertEqual("x1-3", self.browser.cell(0).near(self.browser.cell("x1-0")).under(self.browser.tableHeader("header 4")).text)

    def test_exists(self):
        self.browser.navigate_to(self.base_url  + "/demo/index.htm")
        self.assertTrue(self.browser.link("Link Test").exists())
        self.assertFalse(self.browser.link("Link Test NonExistent").exists())

    def alert1(self, message):
        self.browser.navigate_to(self.base_url  + "/demo/alertTest.htm")
        self.browser.textbox("t1").value = ("Message " + message)
        self.browser.button("Click For Alert").click()
        self.browser.navigate_to("/demo/alertTest.htm")
        time.sleep(1)
        self.assertEqual("Message " + message, self.browser.last_alert())
        self.browser.clear_last_alert()
        self.assertIsNone(self.browser.last_alert())

    def test_alert(self):
        self.alert1("One")
        self.alert1("Two")
        self.alert1("Three")
        self.browser.button("Click For Multiline Alert").click()
        self.assertEqual("You must correct the following Errors:\nYou must select a messaging price plan.\nYou must select an international messaging price plan.\nYou must enter a value for the Network Lookup Charge", self.browser.last_alert())

    def test_confirm(self):
        self.browser.navigate_to(self.base_url  + "/demo/confirmTest.htm")
        self.browser.expect_confirm("Some question?", True)
        self.browser.button("Click For Confirm").click()
        self.assertEqual("oked", self.browser.textbox("t1").value)
        self.browser.navigate_to("/demo/confirmTest.htm")
        time.sleep(1)
        self.assertEqual("Some question?", self.browser.last_confirm())
        self.browser.clear_last_confirm()
        self.assertIsNone(self.browser.last_confirm())

        self.browser.expect_confirm("Some question?", False)
        self.browser.button("Click For Confirm").click()
        self.assertEqual("canceled", self.browser.textbox("t1").value)
        self.assertEqual("Some question?", self.browser.last_confirm())
        self.browser.clear_last_confirm()
        self.assertIsNone(self.browser.last_confirm())

        self.browser.expect_confirm("Some question?", True)
        self.browser.button("Click For Confirm").click()
        self.assertEqual("oked", self.browser.textbox("t1").value)
        self.assertEqual("Some question?", self.browser.last_confirm())
        self.browser.clear_last_confirm()
        self.assertIsNone(self.browser.last_confirm())

    def test_prompt(self):
        self.browser.navigate_to(self.base_url + "/demo/promptTest.htm")
        self.browser.expect_prompt("Some prompt?", "abc")
        self.browser.button("Click For Prompt").click()
        self.assertIsNotNone(self.browser.textbox("t1"))
        self.assertEqual("abc", self.browser.textbox("t1").value)
        self.browser.navigate_to("/demo/promptTest.htm")
        self.browser.wait(20)
        self.assertEqual("Some prompt?", self.browser.last_prompt())
        self.browser.clear_last_prompt()
        self.assertIsNone(self.browser.last_prompt())

    def test_visible(self):
        self.browser.navigate_to(self.base_url  + "/demo/index.htm")
        self.browser.link("Visible Test").click()
        self.assertTrue(self.browser.spandiv("using display").is_visible())

        self.browser.button("Display none").click()
        self.assertFalse(self.browser.spandiv("using display").is_visible())
        self.browser.button("Display block").click()
        self.assertTrue(self.browser.spandiv("using display").is_visible())

        self.browser.button("Display none").click()
        self.assertFalse(self.browser.spandiv("using display").is_visible())
        self.browser.button("Display inline").click()
        self.assertTrue(self.browser.spandiv("using display").is_visible())

        self.assertTrue(self.browser.spandiv("using visibility").is_visible())
        self.browser.button("Visibility hidden").click()
        self.assertFalse(self.browser.spandiv("using visibility").is_visible())
        self.browser.button("Visibility visible").click()
        self.assertTrue(self.browser.spandiv("using visibility").is_visible())

        self.assertFalse(self.browser.byId("nestedBlockInNone").is_visible())
        self.assertFalse(self.browser.byId("absoluteNestedBlockInNone").is_visible())

    def test_check(self):
        self.browser.navigate_to(self.base_url  + "/demo/")
        self.browser.link("Form Test").click()
        self.assertEqual("false", self.browser.checkbox("c1").fetch("checked"))
        self.assertFalse(self.browser.checkbox("c1").is_checked)
        self.browser.checkbox("c1").check()
        self.assertEqual("true", self.browser.checkbox("c1").fetch("checked"))
        self.assertTrue(self.browser.checkbox("c1").is_checked)
        self.browser.checkbox("c1").check()
        self.assertEqual("true", self.browser.checkbox("c1").fetch("checked"))
        self.browser.checkbox("c1").uncheck()
        self.assertEqual("false", self.browser.checkbox("c1").fetch("checked"))
        self.browser.checkbox("c1").uncheck()
        self.assertEqual("false", self.browser.checkbox("c1").fetch("checked"))
        self.browser.checkbox("c1").click()
        self.assertEqual("true", self.browser.checkbox("c1").fetch("checked"))

    def test_focus(self):
        self.browser.navigate_to(self.base_url  + "/demo/focusTest.htm")
        self.browser.textbox("t2").focus()
        self.assertEqual("focused", self.browser.textbox("t1").value)
        self.browser.textbox("t2").remove_focus()
        self.assertEqual("not focused", self.browser.textbox("t1").value)
        self.browser.textbox("t2").focus()
        self.assertEqual("focused", self.browser.textbox("t1").value)

    def test_title(self):
        self.browser.navigate_to(self.base_url  + "/demo/index.htm")
        self.assertEqual("Sahi Tests", self.browser.title)
        self.browser.link("Form Test").click()
        self.assertEqual("Form Test", self.browser.title)
        self.browser.link("Back").click()
        self.browser.link("Window Open Test With Title").click()
        self.assertEqual("With Title", self.browser.popup("With Title").title)

    def test_area(self):
        self.browser.navigate_to(self.base_url  + "/demo/map.htm")
        self.browser.navigate_to("map.htm")
        self.assertTrue(self.browser.area("Record").exists())
        self.assertTrue(self.browser.area("Playback").exists())
        self.assertTrue(self.browser.area("Info").exists())
        self.assertTrue(self.browser.area("Circular").exists())
        self.browser.area("Record").mouse_over()
        self.assertEqual("Record", self.browser.div("output").text)
        self.browser.button("Clear").mouse_over()
        self.assertEqual("", self.browser.div("output").text)
        self.browser.area("Record").click()
        self.assertTrue(self.browser.link("linkByContent").exists())
        #self.browser.navigate_to("map.htm")

    def test_dragdrop(self):
        self.browser.navigate_to("http://www.snook.ca/technical/mootoolsdragdrop/")
        self.browser.div("Drag me").drag_and_drop_on(self.browser.xy(self.browser.div("Item 2"), 5, 5))
        assert self.browser.div("dropped").exists()
        assert self.browser.div("Item 1").exists()
        assert self.browser.div("Item 3").exists()
        assert self.browser.div("Item 4").exists()

    def test_wait(self):
        self.browser.navigate_to(self.base_url  + "/demo/waitCondition1.htm")
        wait_func = lambda: "populated" == self.browser.textbox("t1").value
        self.browser.wait(15, wait_func)
        self.assertEqual("populated", self.browser.textbox("t1").value)

    def test_google(self):
        self.browser.navigate_to("http://www.google.com")
        self.browser.textbox("q").value = "sahi forums"
        self.browser.submit("Google Search").click()
        self.browser.link("Sign In").click()
        assert self.browser.textbox("Form/Email").is_visible()

    def test_dblclick(self):
        self.browser.navigate_to("{}/demo/clicks.htm".format(self.base_url))
        self.browser.div("dbl click me").dblclick()
        self.assertEqual("[DOUBLE_CLICK]", self.browser.textarea("t2").value)
        self.browser.button("Clear").click()

    def test_right_click(self):
        self.browser.navigate_to("{}/demo/clicks.htm".format(self.base_url))
        self.browser.div("right click me").right_click()
        self.assertEqual("[RIGHT_CLICK]", self.browser.textarea("t2").value)
        self.browser.button("Clear").click()

    def test_different_domains(self):
        self.browser.navigate_to("{}/demo/".format(self.base_url))
        self.browser.link("Different Domains External").click()
        domain_tyto = self.browser.domain("www.tytosoftware.com")
        domain_bing = self.browser.domain("www.bing.com")

        domain_tyto.link("Link Test").click()
        domain_bing.textbox("q").value = "fdsfsd"

        domain_tyto.link("Back").click()
        domain_bing.div("bgDiv").click()

        self.browser.navigate_to("{}/demo/".format(self.base_url))

    def test_browser_types(self):
        self.browser.navigate_to("{}/demo/".format(self.base_url))
        if self.browser_name == "firefox":
            self.assertFalse(self.browser.ie())
            self.assertTrue(self.browser.firefox())
        elif self.browser_name == "ie":
            self.assertTrue(self.browser.ie())
            self.assertFalse(self.browser.firefox())

    def test_browser_js(self):
        self.browser.browser_js("function giveMyNumber(){return '23';}")
        self.browser.navigate_to("{}/demo/".format(self.base_url))
        self.assertEqual("23", self.browser.fetch("giveMyNumber()"))
        self.browser.link("Link Test").click()
        self.assertEqual("23", self.browser.fetch("giveMyNumber()"))
        self.browser.link("Back").click()

    def test_count(self):
        self.browser.navigate_to("{}/demo/count.htm".format(self.base_url))
        self.assertEqual(4, self.browser.link("group 0 link").count_similar())
        self.assertEqual(0, self.browser.link("group non existent link").count_similar())
        self.assertEqual(5, self.browser.link("/group 1/").count_similar())
        self.assertEqual(2, self.browser.link("/group 1/").in_(self.browser.div("div1")).count_similar())

    def test_collect(self):
        self.browser.navigate_to("{}/demo/count.htm".format(self.base_url))
        els = self.browser.link("/group 1/").collect_similar()
        self.assertEqual(5, len(els))
        self.assertEqual("group 1 link1", els[0].text)
        self.assertEqual("group 1 link2", els[1].text)

        self.browser.navigate_to("{}/demo/count.htm".format(self.base_url))
        els2 = self.browser.link("/group 1/").in_(self.browser.div("div1")).collect_similar()
        self.assertEqual(2, len(els2))
        self.assertEqual("group 1 link3", els2[0].text)
        self.assertEqual("group 1 link4", els2[1].text)

    def test_strict_visible(self):
        self.browser.navigate_to("{}/demo/strict_visible.htm".format(self.base_url))
        self.assertEqual("b", self.browser.textbox("q[1]").value)
        self.browser.strict_visibility_check(True)
        self.assertEqual("c", self.browser.textbox("q[1]").value)
        self.browser.strict_visibility_check(False)
        self.assertEqual("b", self.browser.textbox("q[1]").value)

    def test_identify_by_multiple_attributes(self):
        self.browser.navigate_to("{}/demo/training/books.htm".format(self.base_url))
        self.browser.textbox("q[2]").value = "aaa"
        self.assertEqual("aaa", self.browser.textbox({"name": "q", "sahiIndex": 2}).value)

    def test_key_press(self):
        self.browser.navigate_to("{}/demo/formTest.htm".format(self.base_url))
        self.browser.textbox("t1").key_press("a")
        self.assertEqual("a", self.browser.textbox("t1").value)
        self.browser.textbox("t1").key_press([66,98])
        self.assertEqual("ab", self.browser.textbox("t1").value)
