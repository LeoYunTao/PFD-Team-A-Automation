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
    # parser.addoption(
    #     '--os', action='store', 
    #     default='windows', help='The os that the testing will be performed on'
    # )
    parser.addoption(
        '--production', action='store', 
        default='false', help='See if the code is in production or testing mode'
    )

@pytest.fixture
def browser(request):
    return request.config.getoption('--browser')

# @pytest.fixture
# def os_system(request):
#     return request.config.getoption('--os')

@pytest.fixture
def production(request):
    return request.config.getoption('--production')

@pytest.fixture
def driver(browser, production):

    if browser == 'firefox':
        options = firefox.options.Options()

        service = None
        if production == 'false':
            service = firefox.service.Service(GeckoDriverManager().install())
        else:
            options.add_argument('--headless')

        driver = webdriver.Firefox(service=service, options=options)
        driver.switch_to.window(driver.current_window_handle)

        return driver

    elif browser == 'chrome':
        options = chrome.options.Options()

        service = None
        if production == 'false':
            service = chrome.service.Service(ChromeDriverManager().install())
        else:
            options.add_argument('--headless')

        driver = webdriver.Chrome(service=service, options=options)
        driver.switch_to.window(driver.current_window_handle)

        return driver

    elif browser == 'edge':
        options = edge.options.Options()

        service = None
        if production == 'false':
            service = edge.service.Service(EdgeChromiumDriverManager().install())
        else:
            options.add_argument('--headless')
        
        driver = webdriver.Edge(service=service, options=options)
        driver.switch_to.window(driver.current_window_handle)

        return driver

    else:
        raise Exception("Browser not found")