import os

from selenium import webdriver

from selenium.webdriver import chrome
from selenium.webdriver import firefox

class Setup:
    @staticmethod
    def initialize_driver(browser, os_system):

        browser_dict = {
            "firefox": {
                "browser_file": "firefox.exe",
                "driver_file": "geckodriver.exe",
                "path": f"drivers/{os_system}/Firefox"
            },
            "chrome": {
                "browser_file": "chrome.exe",
                "driver_file": "chromedriver.exe",
                "path": f"drivers/{os_system}/Chrome"
            }
        }

        browser_file_path = os.path.abspath(browser_dict[browser]['path'])
        
        if browser == "firefox":
            options = firefox.options.Options()
            options.binary_location = os.path.join(browser_file_path, browser_dict[browser]['browser_file'])

            service = firefox.service.Service(os.path.join(browser_file_path, browser_dict[browser]['driver_file']))

            return webdriver.Firefox(options=options, service=service)
        else:
            options = chrome.options.Options()
            options.binary_location = os.path.join(browser_file_path, browser_dict[browser]['browser_file'])

            service = chrome.service.Service(os.path.join(browser_file_path, browser_dict[browser]['driver_file']))

            return webdriver.Chrome(options=options, service=service)
        