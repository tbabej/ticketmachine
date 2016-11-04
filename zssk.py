# -*- coding: utf-8 -*-

from config import config
from patient import PatientBrowser, visible


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
