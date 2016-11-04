# -*- coding: utf-8 -*-
import time
import splinter

from functools import partial
from config import config

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


# with Browser() as browser:
browser = PatientBrowser()
url = 'http://www.slovakrail.sk/'
browser.visit(url)

# Close fancyboy overlay
browser.find_by_id('fancybox-close').click()

# Fill in the search form
browser.fill('from', u'Bratislava hl.st.')
browser.fill('to', u'Košice')
browser.fill('via', u'Zvolen')
browser.fill('date', u'11.11.2016')
browser.fill('time', u'22:00')
browser.find_by_id('vlak_form_big_submit').click()

train_line = browser.find_by_css('.tmp-item-line').first
assert '801' in train_line.html

train_line.find_by_text(u'Nákup dokladu').first.click()
visible(train_line.find_by_text(u'Cestovný lístok')).first.click()

browser.find_by_id('tmp-table-parameters').first.find_by_tag('td').first.click()
browser.find_by_text(u'ŽIAK/ŠTUDENT').first.click()

browser.wait_animation()
browser.click_and_disappear_by_text(u'Pokračovať v nákupe')

browser.new_page()
browser.click_and_disappear_by_text(u'Pokračovať v nákupe')

browser.new_page()
browser.click_and_disappear_by_text(u'Chcem zaplatiť bez prihlásenia alebo registrácie')

browser.new_page()
browser.fill('personalData:payerItemsList:0:field', config.first_name)
browser.fill('personalData:payerItemsList:1:field', config.last_name)
browser.fill('personalData:payerItemsList:2:field', config.street)
browser.fill('personalData:payerItemsList:3:field', config.city)
browser.fill('personalData:payerItemsList:4:field', config.psc)
browser.fill('personalData:payerItemsList2:6:field', config.email)
browser.fill('personalData:payerItemsList2:7:field', config.zssk_card_id)
browser.find_by_text(u'Preniesť údaje platiteľa').first.click()


preukaz_chosen = False
while not u'Registrácia overená' in browser.html:
    browser.slow.fill('personalData:shoppingCartItemList:0:travellerItemsList:0:field', config.first_name)
    browser.slow.fill('personalData:shoppingCartItemList:0:travellerItemsList:1:field', config.surname)
    browser.slow.fill('personalData:shoppingCartItemList:0:travellerItemsList:2:field', config.zssk_card_id)

    if not preukaz_chosen:
        options = browser.find_by_css('.tmp-class')[1]
        options.click()
        browser.wait_animation()
        options.find_by_tag('li')[1].click()
        preukaz_chosen = True

    browser.wait_animation()
    browser.slow.fill('personalData:shoppingCartItemList:0:travellerItemsList:3:field', config.zssk_card_reg)
    browser.slow.find_by_text(u'Over registračné číslo').first.click()
    time.sleep(1)

browser.find_by_text(u'Potvrdzujem, že údaje o cestujúcom/cestujúcich sú správne a súhlasím s poskytnutím osobných údajov pre účely spracovania objednávky cestovných dokladov.').first.click()
browser.click_and_disappear_by_text(u'Pokračovať v platbe')

browser.new_page()
browser.find_by_text(u'Súhlasím s obchodnými podmienkami').first.click()
browser.wait_animation()
browser.click_and_disappear_by_text(u'Pokračovať v nákupe')
