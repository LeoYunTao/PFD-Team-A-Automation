import pandas as pd
import pytest
import platform

from config import URL
from selenium_actions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Form:
    @staticmethod
    def login_details():
        return pd.DataFrame({
            'username': ["Terrence"],
            'password': ["T0491211F"],
        }).to_dict("records")

class TestLogIn:
    @pytest.mark.parametrize("form_input_data", Form.login_details())
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_loginTest(self, driver, os_system, form_input_data):
        selenium_actions = SeleniumActions(driver)
        selenium_actions.login(form_input_data)
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[style="color: red"]')))
        except TimeoutException:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', image_description='Screenshot on success')
            assert True
        else:
            assert False
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='Log in failed')
        finally:
            # close the driver
            driver.quit()
