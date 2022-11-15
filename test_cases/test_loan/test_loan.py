import pytest


from faker import Faker

import random
import platform
import time
import pandas as pd

from config import URL
from selenium_actions import *
import allure


class TestLoanData:

    @staticmethod
    def form_input_data(rows):
        fake = Faker()
        return pd.DataFrame({
            'email': [fake.unique.email() for _ in range(rows)],
            'amount': [random.randint(10000, 20000) for _ in range(rows)],
            'term': [random.randint(0, 1) for _ in range(rows)],
            'income': [random.randint(200000, 450000) for _ in range(rows)],
            'age': [random.randint(20, 30) for _ in range(rows)]
        }).append(pd.DataFrame({
            'email': [fake.unique.email() for _ in range(rows)],
            'amount': [random.randint(10000, 20000) for _ in range(rows)],
            'term': [random.randint(0, 1) for _ in range(rows)],
            'income': [random.randint(200000, 450000) for _ in range(rows)],
            'age': [random.randint(-30, 0) for _ in range(rows)]
        })).to_dict('records')

    @staticmethod
    def generate_test_main(rows=5):
        return TestLoanData.form_input_data(rows)

    @staticmethod
    def generate_test_email(rows=5):
        form_input_datas = TestLoanData.form_input_data(rows)
        form_input_datas.email = pd.Series(['Zachy.aslam@gmail.com', '', 'abc123', None, 'test123.com'])
        return form_input_datas


class TestLoan:

    def common_steps(self, selenium_actions, form_input_data):
        selenium_actions.load_page(URL['loan'], By.TAG_NAME, 'input')

        selenium_actions.fill_form(form_input_data)

    @pytest.mark.parametrize("form_input_data", TestLoanData.form_input_data(rows=5))
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_main(self, os_system, driver, form_input_data):

        selenium_actions = SeleniumActions(driver)

        self.common_steps(selenium_actions, form_input_data)

        if selenium_actions.is_element_located(By.XPATH, '//h1[text()=" You\'ve been approved'
                                                         ' for a loan with UiBank! "]'):
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                               image_description='Screenshot on success')

            driver.quit()
        elif selenium_actions.is_element_located(By.XPATH,'//h1[text()="Sorry, at this time you '
                                                          'have not been approved for a loan."]'):
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                               image_description='Screenshot on success')
            driver.quit()
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                               image_description='Screenshot on failure')
            assert False, "Loan Application Failed"
            driver.quit()

    @pytest.mark.parametrize("form_input_data", TestLoanData.generate_test_email(rows=5))
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_email(self, os_system, driver, form_input_data):

        if form_input_data['email'] == None:
            fake = Faker()
            form_input_data['email'] = fake.unique.email().split("@")[0] + str(random.random())[2:] + "@" + \
                                       fake.unique.email().split("@")[1]
            form_input_data['email'] = form_input_data['email'].split('.')[0]

        selenium_actions = SeleniumActions(driver)

        self.common_steps(selenium_actions, form_input_data)

        if selenium_actions.is_alert_present():
            driver.switch_to.alert.dismiss()
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                               image_description='Screenshot on success')
            driver.quit()
            return

        selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                           image_description='Screenshot on failure')
        driver.quit()
        assert False, f"Email validation failed: {form_input_data['email']}"