from appium.webdriver.common.appiumby import AppiumBy
import time
import json
import sys

class AppInitializer:

    def __init__(self, driver):
        self.driver = driver
        self.f = open("./stringsResources.json")
        self.keys_resources = json.load(self.f)
        self.retries = 0

    def accept_conditions_activity(self):
        self.retriesObserver()
        time.sleep(5)
        try:
            accept_conditions = self.driver.find_element(AppiumBy.XPATH, self.keys_resources[""])
            accept_conditions.click()
            self.retries = 0
        except Exception as e:
            self.retries+=1
            self.accept_conditions_activity()

    def address_button(self):
        self.retriesObserver()
        try:
            time.sleep(5)
            enter_an_adress_btn = self.driver.find_element(AppiumBy.XPATH,self.keys_resources[""] )
            enter_an_adress_btn.click()
            time.sleep(5)
            self.retries = 0
        except Exception as e:
            self.retries+=1
            self.address_button()

    def send_address(self, query: str):
        self.retriesObserver()
        try:
            time.sleep(5)
            enter_adress_input = self.driver.find_element(AppiumBy.ID, self.keys_resources[""])
            time.sleep(5)
            enter_adress_input.send_keys(query)
            self.driver.hide_keyboard()
            self.retries = 0
        except Exception as e:
            self.retries+=1
            time.sleep(3)
            self.send_address(query)

    def select_address(self):
        self.retriesObserver()
        try:
            time.sleep(5)
            select_adress_list = self.driver.find_elements(AppiumBy.ID, self.keys_resources[""])
            if select_adress_list == [] or select_adress_list.__len__() == 0:
                select_adress_list = self.driver.find_elements(AppiumBy.ID, self.keys_resources[""])
            select_adress_list[0].click()
            self.retries = 0
        except Exception as e:
            self.retries += 1
            self.select_address()

    def retriesObserver(self):
        if self.retries >= 20:
            self.driver.quit()
            sys.exit(1)
