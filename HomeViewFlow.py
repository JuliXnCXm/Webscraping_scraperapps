from typing import List
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
import json
import sys
import time
import os

from BusinessFlow import RestaurantFlow
class HomeViewFlow:

    def __init__(self, driver, address, city):
        self.driver = driver
        self.f = open("./stringsResources.json")
        self.keys_resources = json.load(self.f)
        self.screen_dimensions = self.driver.get_window_size()
        self.location_x = self.screen_dimensions["width"] * 0.5
        self.location_start_y = self.screen_dimensions["height"] * 0.7
        self.location_end_y = self.screen_dimensions["height"] * 0.2
        self.duration_scroll = 10
        self.rounds = 0
        self.address = address
        self.city = city
        self.path = self.init_dir()

    def init_dir(self):
        directory = self.address
        parent_dir = "./{}".format(
            self.city)
        self.path = os.path.join(parent_dir, directory)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        return self.path

    def infiniteScroll(self):
        try:
            time.sleep(5)
            self.execute_scrolling()
            restaurant_list = None
            restaurant_list = self.find_restaurants_list()
            restaurant_list_filtered = list(filter(self.filter_restaurants, restaurant_list))
            self.restaurant_iterator(restaurant_list_filtered)
            time.sleep(5)
            self.rounds += 1
            self.roundsObserver()
            self.infiniteScroll()
            self.rounds = 0
        except Exception as e:
            self.rounds += 1
            print(e)

    def execute_scrolling(self):
        touch = TouchAction(self.driver)
        touch.long_press(x=self.location_x, y=self.location_start_y, duration=self.duration_scroll).move_to(x=self.location_x, y=self.location_end_y).release().perform()

    def filter_restaurants(self, restaurant: WebElement):
        print(restaurant.text)
        print(restaurant.is_displayed())
        if restaurant.text.endswith('Min'):
            return True
        else:
            return False

    def find_restaurants_list(self) :
        restaurant_list : list = self.driver.find_element(AppiumBy.ID, "").find_elements( AppiumBy.XPATH, self.keys_resources[""])
        return restaurant_list

    def restaurant_iterator(self , restaurant_list):
        for i in restaurant_list:
            restaurant_flow = RestaurantFlow(
                driver=self.driver,
                screen_dimensions=self.screen_dimensions,
                path=self.path
                )
            i.click()
            time.sleep(5)
            try:
                self.driver.find_element(
                    AppiumBy.ID, self.keys_resources[""])
                print("False Click")
                continue
            except Exception as e:
                header_card = self.driver.find_element(
                AppiumBy.ID, self.keys_resources[""])
                print(header_card)
                restaurant_flow.restaurant_initializer()

    def roundsObserver(self):
        if self.rounds >= 50:
            self.driver.quit()
            sys.exit(1)