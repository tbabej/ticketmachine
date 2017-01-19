import splinter
import time

from functools import partial


class PatientBrowser(object):
    """
    A simple wrapper over Splinter's Browser (which itself is a wrapper around
    Selenium).
    """

    def __init__(self):
        self._browser = splinter.Browser()
        self.__stored_html = None

    def __getattr__(self, name):
        if name.startswith('find_by_'):
            key = name.split('by_')[1]
            return partial(self.generic_wait_and_find, key)
        elif name.startswith('click_and_disappear_by_'):
            key = name.split('by_')[1]
            return partial(self.generic_click_and_disappear, key)

        return getattr(self._browser, name)

    @property
    def slow(self):
        time.sleep(1)
        return self

    def generic_wait_and_find(self, method, *args, **kwargs):
        wait_time = kwargs.get('wait_time')

        if wait_time is not None:
            kwargs.pop('wait_time')
        else:
            wait_time = 20

        is_method = getattr(self, 'is_element_present_by_' + method)
        find_method = getattr(self._browser, 'find_by_' + method)

        if is_method(*args, wait_time=wait_time):
            pass

        return find_method(*args, **kwargs)

    def generic_click_and_disappear(self, method, *args, **kwargs):
        index = kwargs.get('index') or 0
        if index:
            kwargs.pop('index')

        is_method = getattr(self, 'is_element_present_by_' + method)
        find_method = getattr(self, 'find_by_' + method)

        try:
            while is_method(*args, **kwargs):
                element = find_method(*args, **kwargs)[index]
                element.click()
                time.sleep(1)
        except splinter.exceptions.ElementDoesNotExist:
            pass

    def new_page(self):
        while True:
            time.sleep(2)

            if self.html != self.__stored_html:
                self.__stored_html = self.html
                break

    def wait_animation(self):
        time.sleep(2)

def visible(element, timeout=10):
    while not element.visible:
        time.sleep(1)

    return element

def slow(element, sleep=4):
    time.sleep(sleep)
    return element
