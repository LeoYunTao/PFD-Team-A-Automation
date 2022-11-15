import pytest
import pandas as pd

from config import URL
import platform
from selenium_actions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Form:
    @staticmethod
    def loan_details():
        return pd.DataFrame({
            'quoteID': ["637336a5929b090046800455"],
        }).to_dict("records")

class TestLogIn:
    @pytest.mark.parametrize("form_input_data", Form.loan_details())
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_loanStatus(self, driver, os_system, form_input_data):
        selenium_actions = SeleniumActions(driver)
        selenium_actions.load_page(URL['status'], By.TAG_NAME, 'input')
        selenium_actions.fill_form(form_input_data)

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, 'email')))
        except TimeoutException:
            assert False
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='Screenshot on failed')
        else:
            assert True
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='Screenshot on success')
        finally:
            # close the driver
            driver.quit()
