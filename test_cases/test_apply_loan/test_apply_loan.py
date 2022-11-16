import pytest

from faker import Faker

import random
import platform
import time
import pandas as pd

from config import URL
from selenium_actions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestLoanData:

    @staticmethod
    def form_input_data(rows):
        fake = Faker()
        return pd.DataFrame({
            'email': [fake.unique.email() for _ in range(rows)],
            'amount': [random.randint(100, 100000) for _ in range(rows)],
            'term': [random.randint(0, 3) for _ in range(rows)],
            'income': [random.randint(200000, 450000) for _ in range(rows)],
            'age': [random.randint(18, 80) for _ in range(rows)]
        })

    @staticmethod
    def generate_test_main(rows):
        return TestLoanData.form_input_data(rows).to_dict('records')

    @staticmethod
    def generate_test_age(rows):
        form_input_data = TestLoanData.form_input_data(rows)
        invalid_age = pd.Series([random.randint(-30, 17) for _ in range(rows)])
        form_input_data['age'] = invalid_age
        return form_input_data.to_dict('records')

class TestApplyLoan:

    def common_steps(self, selenium_actions, form_input_data):
        selenium_actions.load_page(URL['loan'], By.TAG_NAME, 'input')

        selenium_actions.fill_form(form_input_data)

    @pytest.mark.parametrize("form_input_data", TestLoanData.generate_test_main(rows=int(os.environ['repeat'])))
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_main(self, os_system, driver, form_input_data):

        selenium_actions = SeleniumActions(driver)

        self.common_steps(selenium_actions, form_input_data)

        is_loan_approved = selenium_actions.is_element_located(By.XPATH, '//h1[text()=" You\'ve been approved'
                                                         ' for a loan with UiBank! "]')

        if is_loan_approved:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                               image_description='Screenshot on success')

        # elif selenium_actions.is_element_located(By.XPATH,'//h1[text()="Sorry, at this time you '
        #                                                   'have not been approved for a loan."]'):
        #     selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
        #                                        image_description='Screenshot on success')
        #     driver.quit()
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                               image_description='Screenshot on failure')
        
        driver.quit()
        assert is_loan_approved, "Loan Application Failed"

    @pytest.mark.parametrize("form_input_data", TestLoanData.generate_test_age(rows=int(os.environ['repeat'])))
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_age(self, os_system, driver, form_input_data):

        selenium_actions = SeleniumActions(driver)

        self.common_steps(selenium_actions, form_input_data)

        is_loan_approved = not selenium_actions.is_element_located(By.XPATH, '//h1[text()="Sorry, at this time you have not been approved for a loan."]')

        if is_loan_approved:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                               image_description='Screenshot on failure')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                               image_description='Screenshot on success')

        assert not is_loan_approved, f"Age validation failed: {form_input_data['age']}"