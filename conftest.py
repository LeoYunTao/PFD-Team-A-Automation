import os
import pytest

from selenium import webdriver

from selenium.webdriver import chrome, firefox

from webdriver_manager.firefox import GeckoDriverManager

def pytest_addoption(parser):
    parser.addoption(
        '--browser', action='store', 
        default='chrome', help='The browser to perform testing on'
    )
    parser.addoption(
        '--os', action='store', 
        default='windows', help='The os that the testing will be performed on'
    )

@pytest.fixture
def browser(request):
    return request.config.getoption('--browser')

@pytest.fixture
def os_system(request):
    return request.config.getoption('--os')

@pytest.fixture
def driver(browser, os_system):

    if os_system == 'windows':
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
    else:
        if browser == "firefox":
            options = firefox.options.Options()
            options.add_argument('--headless')

            service = firefox.service.Service(executable_path=os.environ["GECKOWEBDRIVER"])

            return webdriver.Firefox(options=options)
        elif browser == "chrome":

            options = chrome.options.Options()
            options.add_argument('--headless')

            service = chrome.service.Service(executable_path=os.environ["CHROMEWEBDRIVER"])

            return webdriver.Chrome(service=service, options=options)
    