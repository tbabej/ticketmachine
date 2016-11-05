# -*- coding: utf-8 -*-
import time

from ticketmachine.patient import PatientBrowser, visible
from ticketmachine.plugins import Plugin


class ZSSKMachine(Plugin):
    """
    Provides an automation script for buying ZSSK tickets.
    """

    identifier = 'zssk'

    def buy(self, trip, person):
        # with Browser() as browser:
        browser = PatientBrowser()
        url = 'http://www.slovakrail.sk/'
        browser.visit(url)

        # Close fancyboy overlay
        browser.find_by_id('fancybox-close').click()

        # Fill in the search form
        browser.fill('from', trip.start)
        browser.fill('to', trip.end)
        browser.fill('via', trip.via)
        browser.fill('date', trip.date)
        browser.fill('time', trip.time)
        browser.find_by_id('vlak_form_big_submit').click()

        train_line = browser.find_by_css('.tmp-item-line').first

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
        browser.fill('personalData:payerItemsList:0:field', person.first_name)
        browser.fill('personalData:payerItemsList:1:field', person.last_name)
        browser.fill('personalData:payerItemsList:2:field', person.street)
        browser.fill('personalData:payerItemsList:3:field', person.city)
        browser.fill('personalData:payerItemsList:4:field', person.psc)
        browser.fill('personalData:payerItemsList2:6:field', person.email)
        browser.fill('personalData:payerItemsList2:7:field', person.zssk_card_id)
        browser.find_by_text(u'Preniesť údaje platiteľa').first.click()


        preukaz_chosen = False
        while not u'Registrácia overená' in browser.html:
            browser.slow.fill('personalData:shoppingCartItemList:0:travellerItemsList:0:field', person.first_name)
            browser.slow.fill('personalData:shoppingCartItemList:0:travellerItemsList:1:field', person.last_name)
            browser.slow.fill('personalData:shoppingCartItemList:0:travellerItemsList:2:field', person.zssk_card_id)

            if not preukaz_chosen:
                options = browser.find_by_css('.tmp-class')[1]
                options.click()
                browser.wait_animation()
                options.find_by_tag('li')[1].click()
                preukaz_chosen = True

            browser.wait_animation()
            browser.slow.fill('personalData:shoppingCartItemList:0:travellerItemsList:3:field', person.zssk_card_reg)
            browser.slow.find_by_text(u'Over registračné číslo').first.click()
            time.sleep(1)

        browser.find_by_text(u'Potvrdzujem, že údaje o cestujúcom/cestujúcich sú správne a súhlasím s poskytnutím osobných údajov pre účely spracovania objednávky cestovných dokladov.').first.click()
        browser.click_and_disappear_by_text(u'Pokračovať v platbe')

        browser.new_page()
        browser.find_by_text(u'Súhlasím s obchodnými podmienkami').first.click()
        browser.wait_animation()
        browser.click_and_disappear_by_text(u'Pokračovať v nákupe')
