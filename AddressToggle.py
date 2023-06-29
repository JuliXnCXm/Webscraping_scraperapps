import json
import time
from appium.webdriver.webelement import WebElement
from appium.webdriver.common.appiumby import AppiumBy
import sys

class AddressToggle:

    def __init__(self, driver):
        self.driver: WebElement = driver
        self.f = open("./stringsResources.json")
        self.keys_resources = json.load(self.f)
        self.retries = 0

    def _find_address_toggle_btn(self):
        self.retriesObserver()
        try:
            address_toggle_address_btn = self.driver.find_element(
            AppiumBy.ID, self.keys_resources[""])
            address_toggle_address_btn.click()
            self.retries = 0
        except Exception as e:
            self.retries += 1
            time.sleep(3)
            self._find_address_toggle_btn()

    def _select_address(self):
        self.retriesObserver()
        try:
            list_address_recommend_container = self.driver.find_element(
                AppiumBy.ID, self.keys_resources[""]).find_elements(
                AppiumBy.ID, self.keys_resources[""])
            list_address_recommend_container[0].click()
            self.retries = 0
        except:
            self.retries += 1
            time.sleep(3)
            self._select_address()

    def retriesObserver(self):
        if self.retries >= 20:
            print("Error: Quitting")
            self.driver.quit()
            sys.exit(1)