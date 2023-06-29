import json
from appium.webdriver.webelement import WebElement
from appium.webdriver.common.appiumby import AppiumBy
import time
import re
import sys
import requests
from dotenv import load_dotenv
import os
import random

class RestaurantFlow:

    def __init__(self, driver, screen_dimensions, path):
        self.driver = driver
        self.f = open("./stringsResources.json")
        self.keys_resources = json.load(self.f)
        self.screen_dimensions = screen_dimensions
        self.location_x = self.screen_dimensions["width"] * 0.5
        self.location_start_y = self.screen_dimensions["height"] * 0.7
        self.location_end_y = self.screen_dimensions["height"] * 0.1
        self.duration_scroll = 10
        self.basic_details = None
        self.extra_details = None
        self._rating = None
        self._business_name = None
        self._delivery_fee = None
        self._delivery_time = None
        self._working_hours = None
        self.restaurant_closed = False
        self._address = None
        self.path = path
        self._latLng = None
        self.retries = 0

    def restaurant_initializer(self):
        self.got_it_btn()
        self.restaurant_basic_detail()
        self.show_restaurant_info_card()
        time.sleep(2)
        self.restaurant_extra_detail()
        self.hide_restaurant_info_card()
        self.driver.back()
        return self.restaurant_builder_data()

    def show_restaurant_info_card(self):
        global business_detail_is_displayed
        business_detail_is_displayed = False
        header_card: WebElement = self.driver.find_element(
            AppiumBy.ID, self.keys_resources[""])
        header_card.click()
        time.sleep(2)
        try:
            business_detail: WebElement = self.driver.find_element(
            AppiumBy.ID, self.keys_resources[""])
            business_detail_is_displayed = business_detail.is_displayed()
            if business_detail_is_displayed == True:
                self.retries = 0
        except:
            self.retries += 1
            self.retriesObserver()
            business_detail_is_displayed = False
            self.show_restaurant_info_card()
        return business_detail_is_displayed

    def hide_restaurant_info_card(self):
        global header_card_is_displayed
        header_card_is_displayed = False
        close_btn_card: WebElement = self.driver.find_element(
            AppiumBy.ID, self.keys_resources[""])
        close_btn_card.click()
        try:
            header_card: WebElement = self.driver.find_element(
            AppiumBy.ID, self.keys_resources[""])
            header_card_is_displayed = header_card.is_displayed()
            if header_card_is_displayed == True:
                self.retries = 0
        except:
            self.retries += 1
            self.retriesObserver()
            header_card_is_displayed = False
            self.hide_restaurant_info_card()
        return header_card_is_displayed

    def restaurant_basic_detail(self):
        try:
            header_card: WebElement = self.driver.find_element(AppiumBy.ID, self.keys_resources[""])
            list_elements = header_card.find_elements(
                AppiumBy.CLASS_NAME, "android.widget.TextView")
            self.basic_info_retriever(list_elements, True)
            self.retries = 0
        except:
            self.retries += 1
            self.retriesObserver()
            time.sleep(2)
            self.restaurant_basic_detail()

    def basic_info_retriever(self, header_card_elements , isBasicInfo):
        header_card_elements_mapped = list(map(lambda x: " ".join(re.findall(
            "[a-zA-Z.0-9$#-]+", x.text)), header_card_elements))
        if header_card_elements_mapped[0].startswith('Closed') or header_card_elements_mapped[0].startswith('Tempora') or header_card_elements_mapped[0].startswith('Outside'):
            self.restaurant_closed = True
        if isBasicInfo == True:
            self.basic_details = list(filter(self.clean_values, header_card_elements_mapped))
            self.__retrieve_business_name()
            self.__retrieve_rating()
            self.__retrieve_delivery_time()
            self.__retrieve_delivery_fee()
        else:
            try:
                self.extra_details = list(filter(self.clean_values, header_card_elements_mapped))
                self.__retrieve_working_hours()
                self.__retrieve_address()
            except Exception as e:
                print(e)

    def clean_values(self,value_to_clean):
        if value_to_clean == "":
            return False
        if value_to_clean.startswith("Sale"):
            return False
        if value_to_clean.startswith("Buy"):
            return False
        else:
            return True

    def restaurant_extra_detail(self):
        try:
            business_detail: WebElement = self.driver.find_element(
                AppiumBy.ID, self.keys_resources["BUSINESS_DETAIL"])
            list_elements = business_detail.find_elements(
                AppiumBy.CLASS_NAME, "android.widget.TextView")
            self.basic_info_retriever(list_elements, False)
            self.retries = 0
        except:
            self.retries += 1
            self.retriesObserver()
            time.sleep(2)
            self.restaurant_extra_detail()

    def got_it_btn(self):
        try:
            got_it_btn: WebElement = self.driver.find_element(
                AppiumBy.ID, self.keys_resources[""])
            time.sleep(5)
            got_it_btn.click()
        except Exception as e:
            print("No got it button founded")

    def index_finder(self, query): return [x for x in range(len(self.basic_details)) if self.basic_details[x].startswith(query)][0]

    def index_finder_extra(self, query): return [x for x in range(len(self.extra_details)) if self.extra_details[x].startswith(query)][0]

    # BASIC DETAILS --------------------------------

    def __retrieve_rating(self):
        try:
            self._rating = self.basic_details[self.index_finder("Rat")+1]
        except:
            self._rating = "No rating available"

    def __retrieve_delivery_time(self):
        try:
                self._delivery_time = self.basic_details[self.index_finder("")+1]
        except:
            self._delivery_time = "No delivery time available"

    def __retrieve_delivery_fee(self):
        try:
            self._delivery_fee = self.basic_details[self.index_finder("Delivery")+1]
        except:
            self._delivery_fee = "No delivery fee available"

    def __retrieve_business_name(self):
        try:
            if self.restaurant_closed == True:
                self._business_name = self.basic_details[1]
            else:
                self._business_name = self.basic_details[0]
        except:
            self._business_name = "No business name available"

    # EXTRA DETAILS --------------------------------

    def __retrieve_address(self):
        try:
            self._address = self.extra_details[self.index_finder_extra("Addr")+1]
        except:
            self._address = "No address available"
        # self.__retrieve_latitude_longitude()

    def __retrieve_working_hours(self):
        try:
            self._working_hours = " ".join(
            self.extra_details[self.index_finder_extra("Busi")+1: self.index_finder_extra("Deli")])
        except:
            self._working_hours = "No working hours available"

    def __retrieve_latitude_longitude(self):
        CITY = ""
        try:
            locationObj = self._address.replace('#', '')
            if "" not in locationObj:
                locationObj = locationObj + ", {}".format(CITY)
            if "" not in locationObj or "" not in locationObj:
                locationObj= locationObj + ", country"
            resp = requests.get("{URI}?key={KEY}&location={LOCATION}".format(URI=os.getenv(
                "GEOCODING_ADDRESS_URI"), KEY=os.getenv("ACCESS_KEY_GEOCODING"), LOCATION=locationObj))
            if resp.status_code == 200:
                results = resp.json()
                self._latLng =  results["results"]
        except:
                self._latLng =  "No Geo found"

    def restaurant_builder_data(self):
        data = {
            "name": self._business_name,
            "rating": self._rating,
            "address": self._address,
            "working_hours": self._working_hours,
            "latLng": self._latLng,
        }

        file_path = os.path.join(self.path, data[""] + ".json")
        if not os.path.exists(file_path):
            json_object = json.dumps(data)
            f = open(file_path, "w")
            f.write(json_object)
            f.close()
        self.restaurant_closed = False

    def retriesObserver(self):
        if self.retries >= 10:
            self.driver.quit()
            sys.exit(1)