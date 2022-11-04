import pytest

from selenium import webdriver
from selenium.webdriver import chrome, firefox, edge

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

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

    if os_system == "linux":
        if browser == "firefox":
            driver = webdriver.Firefox()
            driver.switch_to.window(driver.current_window_handle)

            return driver

        elif browser == "chrome":
            driver = webdriver.Chrome()
            driver.switch_to.window(driver.current_window_handle)

            return driver

        elif browser == "edge":
            driver = webdriver.Edge()
            driver.switch_to.window(driver.current_window_handle)

            return driver
    else:
        if browser == "firefox":
            options = firefox.options.Options()

            service = firefox.service.Service(GeckoDriverManager().install())

            driver = webdriver.Firefox(service=service, options=options)
            driver.switch_to.window(driver.current_window_handle)

            return driver

        elif browser == "chrome":

            options = chrome.options.Options()

            service = chrome.service.Service(ChromeDriverManager().install())

            driver = webdriver.Chrome(service=service, options=options)
            driver.switch_to.window(driver.current_window_handle)

            return driver

        elif browser == "edge":
            options = edge.options.Options()

            service = edge.service.Service(EdgeChromiumDriverManager().install())

            driver = webdriver.Edge(service=service, options=options)
            driver.switch_to.window(driver.current_window_handle)

            return driver