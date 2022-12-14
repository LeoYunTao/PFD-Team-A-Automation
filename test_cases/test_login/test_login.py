import pytest

import pandas as pd
import platform

from faker import Faker

from selenium_actions import *
from config import URL

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Form:
    @staticmethod
    def generate_test_password():
        fake = Faker()

        return pd.DataFrame({
            'username': ["yt"],
            'password': [fake.unique.password()],
        }).to_dict("records")

class TestLogin:
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_main(self, driver, os_system, login_details):
        
        selenium_actions = SeleniumActions(driver)
        selenium_actions.login(login_details)

        assert URL['main'] == driver.current_url
        driver.quit()

    @pytest.mark.parametrize("form_input_data", Form.generate_test_password())
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_password(self, driver, os_system, form_input_data):
        selenium_actions = SeleniumActions(driver)
        selenium_actions.login(form_input_data)

        assert URL['main'] != driver.current_url
        driver.quit()
