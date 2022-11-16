import pytest

import pandas as pd
import time
import platform

from config import URL
from selenium_actions import *

from faker import Faker

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Form:

    @staticmethod
    def generate_false_id(rows=5):
        fake = Faker()
        return pd.DataFrame({
            'quoteID': [fake.unique.uuid4().replace('-', '') for _ in range(rows)]
        }).to_dict("records")

class TestLoanStatus:

    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_main(self, driver, os_system, quote_id):
        selenium_actions = SeleniumActions(driver)
        
        selenium_actions.load_page(URL['status'], By.TAG_NAME, 'input')
        
        selenium_actions.fill_form(quote_id)

        is_view_loan_detail_successful = selenium_actions.is_element_located(By.ID, 'email')

        if is_view_loan_detail_successful:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='Screenshot on success')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='Screenshot on failure')
        
        driver.quit()

        assert is_view_loan_detail_successful

    @pytest.mark.parametrize("form_input_data", Form.generate_false_id(rows=5))
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_quote_id(self, driver, os_system, form_input_data):
        selenium_actions = SeleniumActions(driver)
        
        selenium_actions.load_page(URL['status'], By.TAG_NAME, 'input')
        
        selenium_actions.fill_form(form_input_data)

        is_view_loan_detail_successful = not selenium_actions.is_element_located(By.XPATH, '//h1[text()="Sorry! We weren\'t able to locate a matching loan ID. "]')

        if is_view_loan_detail_successful:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='Screenshot on failure')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='Screenshot on success')
        
        driver.quit()

        assert not is_view_loan_detail_successful
