# libraries imports
import os
from appium import webdriver
from dotenv import load_dotenv
import logging
import sys
import argparse
import pandas as pd
import time
# custom imports
from AppInitializer import AppInitializer
from HomeViewFlow import HomeViewFlow
from AddressToggle import AddressToggle
from appium.webdriver.common.appiumby import AppiumBy

def run(args):

    global data
    data = {
        "address_list": []
    }
    if args.type_file_path == True:
        logging.info('Beginning Appium scrapping process for text addresses repository in path {}'.format(args.resource))
        if args.resource[-3:] == "csv":
            data = pd.read_csv(args.resource, delimiter=",")
        else:
            data = pd.read_json(args.resource)["addresses_list"].values
    else:
        logging.info('Beginning Appium scrapping process for single address {}'.format(args.resource))
        data["address_list"] = args.resource

    logger = logging.getLogger(__name__)
    load_dotenv()
    global driver
    driver = {
        "platformName": os.getenv("PLATFORM_NAME"),
        "platformVersion": os.getenv("PLATFORM_VERSION"),
        "deviceName": os.getenv("DEVICE_NAME"),
        "automationName": os.getenv("AUTOMATION_NAME"),
        "appPackage": os.getenv("APP_PACKAGE"),
        "appActivity": os.getenv("APP_ACTIVITY"),
        "noReset":  os.getenv("NO_RESET"),
        "fullReset":  os.getenv("FULL_RESET"),
        "ensureWebviewsHavePages": os.getenv("ENSURE_WEB_VIEWS_HAVE_PAGES")
    }
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", driver)

    if driver:
        logger.info('Driver set up successfully')
    else:
        logger.info('Driver set up failed')
        logger.info('Exit process -> ')
        sys.exit(1)
    global initializer
    initializer = AppInitializer(driver=driver)
    # Init AppInitializer class
    if os.getenv("NO_RESET") == "false":
        logger.info('No reset capability is false, skipping authentication process')
        logger.info('workflow will be initialized for not logged user')
        initializer.accept_conditions_activity()
        initializer.address_button()
        initializer.send_address("")
        initializer.select_address()

def popup_in_home():
    try:
        popup = driver.find_element(AppiumBy.ID, initializer.keys_resources[""])
        if popup.is_displayed == True:
            popup_btn = driver.find_element(
                AppiumBy.ID, initializer.keys_resources[""])
            popup_btn.click()
            time.sleep(2)
    except:
        print("No popup present!")

def update_popup_in_home():
    try:
        popup_close_button = driver.find_element(
            AppiumBy.ID, initializer.keys_resources[""])
        if popup_close_button.is_displayed == True:
            popup_close_button.click()
            time.sleep(2)
    except:
        print("No popup present!")

def addresses_iterator():
    address_toggle = AddressToggle(driver=driver)
    for address in data:
        homeflow = HomeViewFlow(driver=driver, address=address, city="BOGOTA")
        print("loading data...")
        time.sleep(30)
        popup_in_home()
        print(address)
        update_popup_in_home()
        address_toggle._find_address_toggle_btn()
        time.sleep(5)
        initializer.send_address(address)
        address_toggle._select_address()
        confirm_btn = driver.find_element(
            AppiumBy.ID, initializer.keys_resources[""])
        confirm_btn.click()
        skip_confirm_btn = driver.find_element(AppiumBy.ID,
                            initializer.keys_resources[""]).find_element(AppiumBy.XPATH, initializer.keys_resources[""])
        skip_confirm_btn.click()
        time.sleep(10)
        homeflow.infiniteScroll()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process for scrape information from an android application usin Appium and python")
    def file_choices(choices,fname):
        ext = os.path.splitext(fname)[1][1:]
        if ext not in choices:
            parser.error("file doesn't end with one of {}".format(choices))
        return fname

    parser.add_argument('-f',
                        help='Scrape using file path',
                        action='store_true',
                        dest="type_file_path"
                        )
    parser.add_argument('-s',
                        help='Scrape using the string specified',
                        action='store_true',
                        dest="type_string"
                        )
    namespace = parser.parse_known_args()
    parser.add_argument('resource',
                        help='Addresses file path or string to scrape',
                        type=lambda s: file_choices(("csv", "json"), s) if namespace[0].__dict__[
                            "type_file_path"] == True else str,
                        )
    args = parser.parse_args()
    run(args)
    addresses_iterator()