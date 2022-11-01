import os

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class Setup:
    @staticmethod
    def initialize_driver(browser, os_system):

        browser_dict = {
            "firefox": {
                "browser_file": "chrome.exe",
                "driver_file": "chromedriver.exe",
                "path": f"drivers/{os_system}/Chrome"
            },
            "chrome": {
                "browser_file": "chrome.exe",
                "driver_file": "chromedriver.exe",
                "path": f"drivers/{os_system}/Firefox"
            }
        }

        chrome_file_path = os.path.abspath(f"drivers/{os_system}/Chrome")

        options = Options()
        options.binary_location = os.path.join(chrome_file_path, browser_dict[browser]['browser_file'])
        
        return webdriver.Chrome(options=options, service=Service(os.path.join(chrome_file_path, browser_dict[browser]['driver_file'])))
        