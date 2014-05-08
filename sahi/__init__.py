import requests
import uuid
import time


class Browser(object):
    def __init__(self, *args):
        self.proxy_host = 'localhost'
        self.proxy_port = 9999
        if len(args) == 3:
            self.browser_path = args[0]
            self.browser_options = args[1]
            self.browser_executable = args[2]
        elif len(args) == 1:
            self.browser_type = args[0]
        self.popup_name = None
        self.domain_name = None
        self.sahisid = None
        self.print_steps = False

    def __getattr__(self, item):
        def element(*args):
            return Element(self, item, *args)
        return element

    def check_proxy(self):
        try:
            requests.get('http://{}:{}/_s_/spr/blank.htm'.format(
                self.proxy_host, self.proxy_port))
        except requests.ConnectionError:
            raise "Sahi proxy is not available. Please start the Sahi proxy."

    def open(self):
        self.check_proxy()
        self.sahisid = time.time()
        self.start_url = "http://sahi.example.com/_s_/dyn/Driver_initialized"
        if (self.browser_type is not None ):
            self.exec_command("launchPreconfiguredBrowser", {
                "browserType": self.browser_type,
                "startUrl": self.start_url
            })
        else:
            self.exec_command("launchAndPlayback", {
                "browser": self.browser,
                "browserOptions": self.browser_options,
                "browserExecutable": self.browser_executable,
                "startUrl": self.start_url
            })
        for i in range(500):
            if self.is_ready():
                break
                time.sleep(0.1)

    def is_ready(self):
        return self.exec_command('isReady') == 'true'

    def exec_command(self, command, qs=None):
        if qs is None:
            qs = {}
        qs.update({'sahisid': self.sahisid})
        res = requests.get('http://{}:{}/_s_/dyn/Driver_{}'.format(
            self.proxy_host, self.proxy_port, command), params=qs)
        return res.text

    def response(self, url, qs={}):
        return requests.post(url, data=qs).text

    def navigate_to(self, url, force_reload=False):
        self.execute_step(''.join((
            '_sahi._navigateTo("', url, '", ', str(force_reload).lower(),
            ')')))

    def execute_step(self, step):
        if self.has_popup():
            step = '_sahi._popup({}).{}'.format(quoted(self.popup_name), step)
        if self.has_domain():
            step = '_sahi._domain({}).{}'.format(quoted(self.domain_name),
                                                 step)
        self.exec_command("setStep", {"step": step})
        for i in range(500):
            time.sleep(0.1)
            response = self.exec_command("doneStep")
            if response == 'true':
                return True
            elif response.startswith('error:'):
                raise Exception(response)

    # evaluates a javascript expression on the browser and fetches its value
    def fetch(self, expression):
        key = "___lastValue___" + str(uuid.uuid4())
        self.execute_step(
            "_sahi.setServerVarPlain('" + key + "', " + expression + ")")
        return self.check_nil(self.exec_command("getVariable", {"key": key}))

    # evaluates a javascript expression on the browser and returns true if value is true or "true"
    def fetch_boolean(self, expression):
        result = self.fetch(expression) == "true"
        return self.fetch(expression) == "true"

    # # returns element attributes of all elements of type attr matching the identifier within relations
    def collect(self, els, attribute=None):
        if attribute is None:
            return els.collect_similar()
        else:
            return self.fetch("_sahi.collectAttributes({}, {}, {})".format(
                quoted(attribute),
            )).split(",___sahi___")
            return fetch("_sahi.collectAttributes(#{Utils.quoted(attr)}, #{Utils.quoted(els.to_type())}, #{els.to_identifiers()})").split(",___sahi___")


    def browser_js(self, value):
        self.exec_command("setBrowserJS", {"browserJS": value})

    def check_nil(self, string):
        if string == "null":
            return None
        return string

    # closes the browser
    def close(self):
        if self.has_popup():
            self.execute_step("_sahi._closeWindow()")
        else:
            self.exec_command("kill")

    def speed(self, value):
        self.exec_command("setSpeed", {"speed": value})

    def strict_visibility_check(self, value):
        self.execute_step("_sahi._setStrictVisibilityCheck({})".format(str(value).lower()))

    # represents a popup window. The name is either the window name or its title.
    def popup(self, name):
        if self.browser_type is not None:
            win = Browser(self.browser_type)
        else:
            win = Browser(self.browser_path, self.browser_options,
                          self.browser_executable)
        win.proxy_host = self.proxy_host
        win.proxy_port = self.proxy_port
        win.sahisid = self.sahisid
        win.print_steps = self.print_steps
        win.popup_name = name
        win.domain_name = self.domain_name
        return win

    # represents a domain section of window.
    def domain(self, name):
        if self.browser_type is not None:
            win = Browser(self.browser_type)
        else:
            win = Browser(self.browser_path, self.browser_options,
                          self.browser_executable)
        win.proxy_host = self.proxy_host
        win.proxy_port = self.proxy_port
        win.sahisid = self.sahisid
        win.print_steps = self.print_steps
        win.popup_name = self.popup_name
        win.domain_name = name
        return win

    def has_popup(self):
        return self.popup_name is not None

    def has_domain(self):
        return self.domain_name is not None

    def last_alert(self):
        return self.fetch("_sahi._lastAlert()")

    # resets the last alerted message
    def clear_last_alert(self):
        self.execute_step("_sahi._clearLastAlert()")

    # returns the last confirm message
    def last_confirm(self):
        return self.fetch("_sahi._lastConfirm()")

    # resets the last confirm message
    def clear_last_confirm(self):
        self.execute_step("_sahi._clearLastConfirm()")

    # set an expectation to press OK (true) or Cancel (false) for specific confirm message
    def expect_confirm(self, message, input):
        input = str(input).lower()
        self.execute_step(
            '_sahi._expectConfirm({}, {})'.format(quoted(message), input))

    # returns the last prompted message
    def last_prompt(self):
        return self.fetch("_sahi._lastPrompt()")

    # clears the last prompted message
    def clear_last_prompt(self):
        self.execute_step("_sahi._clearLastPrompt()")

    # set an expectation to set given value for specific prompt message
    def expect_prompt(self, message, input):
        self.execute_step(
            '_sahi._expectPrompt({}, {})'.format(quoted(message), quoted(input)))

    # simulates the touch event
    # def touch()
    #   execute_step("_sahi._touch(#{self.to_s()})")
    # end
    #
    # # simulates the tap event
    # def tap()
    #   execute_step("_sahi._tap(#{self.to_s()})")
    # end
    #
    # # simulates the touchStart event
    # def touchStart()
    #   execute_step("_sahi._touchStart(#{self.to_s()})")
    # end
    #
    # # simulates the touchEnd event
    # def touchEnd()
    #   execute_step("_sahi._touchEnd(#{self.to_s()})")
    # end
    #
    # # simulates the touchCancel event
    # def touchCancel()
    #   execute_step("_sahi._touchCancel(#{self.to_s()})")
    # end
    #
    # # simulates the touchMove event
    # def touchMove(moveX, moveY, isRelative=true)
    #   execute_step("_sahi._touchMove(#{self.to_s()}, moveX, moveY, isRelative)")
    # end
    #
    # # simulates the swipe event
    # def swipe(moveX, moveY, isRelative=true)
    #   execute_step("_sahi._touchMove(#{self.to_s()}, moveX, moveY, isRelative)")
    # end

    # get last downloaded file's name
    def last_downloaded_filename(self):
        return self.fetch("_sahi._lastDownloadedFileName()")

    # clear last downloaded file's name
    def clear_last_downloaded_filename(self):
        self.execute_step("_sahi._clearLastDownloadedFileName()")

    # Save the last downloaded file to specified path
    def save_downloaded(self, file_path):
        self.execute_step(
            '_sahi._saveDownloadedAs({})'.format(quoted(file_path)))

    # make specific url patterns return dummy responses. Look at _addMock documentation.
    def add_url_mock(self, url_pattern, clazz=None):
        if clazz is None:
            clazz = "MockResponder_simple"
        self.execute_step("_sahi._addMock({}, {})".format(quoted(url_pattern),
                                                          quoted(clazz)))

    # reverse effect of add_url_mock
    def remove_url_mock(self, url_pattern):
        self.execute_step("_sahi._removeMock({})".format(quoted(url_pattern)))

    # return window title
    @property
    def title(self):
        return self.fetch("_sahi._title()")

    # returns true if browser is Internet Explorer
    def ie(self):
        return self.fetch_boolean("_sahi._isIE()")

    def firefox(self):
        return self.fetch_boolean("_sahi._isFF()")

    def chrome(self):
        return self.fetch_boolean("_sahi._isChrome()")

    def safari(self):
        return self.fetch_boolean("_sahi._isSafari()")

    def opera(self):
        return self.fetch_boolean("_sahi._isOpera()")

    def wait(self, timeout, func=None):
        if func is None:
            time.sleep(timeout)
        else:
            total = 0;
            interval = 0.2;
            while total < timeout and not func():
                time.sleep(interval)
                total += interval



class Element(object):
    actions = {
        "click": "click",
        "focus": "focus",
        "remove_focus": "removeFocus",
        "check": "check",
        "uncheck": "uncheck",
        "dblclick": "doubleClick",
        "right_click": "rightClick",
        "key_down": "keyDown",
        "key_up": "keyUp",
        "mouse_over": "mouseOver",
        "mouse_down": "mouseDown",
        "mouse_up": "mouseUp"
    }

    def __init__(self, browser, type, *args):
        self.browser = browser
        self.type = type
        if len(args) == 1 and isinstance(args[0], list):
            self.identifiers = args[0]
        else:
            self.identifiers = list((args))

    def __str__(self):
        return "_sahi._{}({})".format(self.type, ', '.join(
            self.concat_identifiers(self.identifiers)))

    def __getattr__(self, item):
        if item in self.actions:
            def perform():
                step = "_sahi._{}({})".format(self.actions[item], self)
                self.browser.execute_step(step)
            return perform

    def key_press(self, codes, combo=None):
        if combo is None:
            combo = "null"
        if isinstance(codes, str):
            self.browser.execute_step('_sahi._keyPress({}, {}, "{}")'.format(
                self, quoted(codes), combo
            ))
        else:
            self.browser.execute_step('_sahi._keyPress({}, {}, "{}")'.format(
            self, list_to_string(codes), combo
        ))

    # drag element and drop on another element
    def drag_and_drop_on(self, el2):
        self.browser.execute_step("_sahi._dragDrop({}, {})".format(self, el2))

    def choose(self, value):
        if isinstance(value, list):
            value = '["{}"]'.format('","'.join(value))
            self.browser.execute_step("_sahi._setSelected({}, {})".format(self, value))
        else:
            self.browser.execute_step("_sahi._setSelected({}, {})".format(self, quoted(value)))

    # returns value of textbox or textareas and other relevant input elements
    @property
    def value(self):
        return self.browser.fetch("{}.value".format(self))

    # sets the value for textboxes or textareas. Also triggers necessary events.
    @value.setter
    def value(self, value):
        self.browser.execute_step(
            "_sahi._setValue({}, {})".format(self, quoted(value)))

    # fetches value of specified attribute
    def fetch(self, attribute=None):
        if attribute is None:
            return self.browser.fetch("{}".format(self))
        return self.browser.fetch("{}.{}".format(self, attribute))

    # returns boolean value of attribute. returns true only if fetch returns "true"
    def fetch_boolean(self, attribute=None):
        return self.browser.fetch_boolean(attribute)


    # Emulates setting filepath in a file input box.
    def file(self, value):
        self.browser.execute_step("_sahi._setFile({}, {})".format(self, quoted(value)))

    @property
    def text(self):
        return self.browser.fetch("_sahi._getText({})".format(self))

    @property
    def is_checked(self):
        return self.fetch("checked") == "true"

    # returns selected text from select box
    def selected_text(self):
        return self.browser.fetch("_sahi._getSelectedText({})".format(self))

    # returns a stub with a DOM "near" relation to another element
    # Eg.
    #  browser.button("delete").near(browser.cell("User One")) will denote the delete button near the table cell with text "User One"
    def near(self, el2):
        self.identifiers.append(Element(self.browser, "near", [el2]))
        return self

    # returns a stub with a DOM "in" relation to another element
    # Eg.
    #  browser.image("plus.gif").in(browser.div("Tree Node 2")) will denote the plus icon inside a tree node with text "Tree Node 2"
    def in_(self, el2):
        self.identifiers.append(Element(self.browser, "in", [el2]))
        return self

    def _positional(self, method, element, offset=None, limit_under=None):
        if offset is not None or limit_under is not None:
            identifiers = [element, offset, limit_under]
        else:
            identifiers = [element]
        self.identifiers.append(Element(self.browser, method, identifiers))
        return self

    def under(self, element, offset=None, limit_under=None):
        return self._positional('under', element, offset, limit_under)

    def above(self, element, offset=None, limit_under=None):
        return self._positional('above', element, offset, limit_under)

    def above_or_under(self, element, offset=None, limit_under=None):
        return self._positional('aboveOrUnder', element, offset, limit_under)

    def right_of(self, element, offset=None, limit_under=None):
        return self._positional('rightOf', element, offset, limit_under)

    def left_of(self, element, offset=None, limit_under=None):
        return self._positional('leftOf', element, offset, limit_under)

    def left_or_right_of(self, element, offset=None, limit_under=None):
        return self._positional('leftOrRightOf', element, offset, limit_under)

    # specifies exacts coordinates to click inside an element. The coordinates are relative to the element. x is from left and y is from top. Can be negative to specify other direction
    # browser.button("Menu Button with Arrow on side").xy(-5, 10).click will click on the button, 5 pixels from right and 10 pixels from top.
    def xy(self, x, y):
        return Element(self, "xy", [self, x, y])

    # denotes the DOM parentNode of element.
    # If tag_name is specified, returns the parent element which matches the tag_name
    # occurrence finds the nth parent of a particular tag_name
    # eg. browser.cell("inner nested cell").parent_node("TABLE", 3) will return the 3rd encapsulating table of the given cell.
    def parent_node(self, tag_name="ANY", occurrence=1):
        return Element(self.browser, "parentNode", [self]);

    # returns true if the element exists on the browser
    def exists(self, optimistic=False):
        if optimistic:
            return self.exists1()
        for i in range(5):
            if self.exists1():
                return True
        return False

    def exists1(self):
        return self.browser.fetch("_sahi._exists({})".format(self)) == 'true'

    # returns true if the element exists and is visible on the browser
    def is_visible(self, optimistic=False):
        if optimistic:
            return self.is_visible1()
        for i in range(5):
            if self.is_visible1():
                return True
        return False

    def is_visible1(self):
        return self.browser.fetch(
            "_sahi._isVisible({})".format(self)) == 'true'

    # returns true if the element contains this text
    def contains_text(self, text):
        return self.browser.fetch(
            "_sahi._containsText({}, {})".format(self, quoted(text)))

    # returns true if the element contains this html
    def contains_html(self, html):
        return self.browser.fetch(
            "_sahi._containsHTML({}, {})".format(self, quoted(html)))

    # returns count of elements similar to this element
    def count_similar(self):
        return int(self.browser.fetch('_sahi._count("_{}", {})'.format(
            self.type, ', '.join(self.concat_identifiers(self.identifiers)))))

    # # returns array elements similar to this element
    def collect_similar(self):
        count = self.count_similar()
        els = []
        for i in range(count):
            copy = list(self.identifiers)
            copy[0] = "{}[{}]".format(copy[0], i)
            els.append(Element(self.browser, self.type, copy))
        return els

    def concat_identifiers(self, ids):
        def id_to_string(id):
            if isinstance(id, str):
                return quoted(id)
            elif isinstance(id, list):
                return list_to_string(id)
            elif id is None:
                return 'null'
            else:
                return str(id)

        return [id_to_string(id) for id in ids]

    def to_type(self):
        return '_{}'.format(self.type)


def list_to_string(list_):
    return '[{}]'.format(','.join(str(item) for item in list_))


def quoted(string):
    return "\"" + string.replace("\\", "\\\\").replace("\"", "\\\"") + "\""
