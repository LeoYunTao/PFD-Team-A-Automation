import pytest
import platform
import pandas as pd
import time

import os

from faker import Faker
import random

from config import URL
from selenium_actions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

class Form:

    @staticmethod
    def account_details(rows=5):
        fake = Faker()
        return pd.DataFrame({
            'accountNickname': [fake.unique.user_name() for _ in range(rows)],
            'typeOfAccount': [random.randint(0, 1) for _ in range(rows)],
        }).to_dict("records")

    @staticmethod
    def generate_test_type_of_account():
        fake = Faker()
        return pd.DataFrame({
            'accountNickname': [fake.unique.user_name()],
        }).to_dict("records")

    
class TestApplyAccount:

    def common_steps(self, driver, selenium_actions, login_details, form_input_data):
        selenium_actions.login(login_details)
        
        applyAccountPage = driver.find_element(By.XPATH, '//div[text()="Apply For New Account"]')
        applyAccountPage.click()

        assert selenium_actions.is_element_located(By.XPATH, '//h1[text()="Apply For A New Account"]')

        selenium_actions.fill_form(form_input_data)

    @pytest.mark.parametrize("form_input_data", Form.account_details(rows=int(os.environ['repeat'])))
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_main(self, driver, os_system, login_details, form_input_data):

        selenium_actions = SeleniumActions(driver)
        
        self.common_steps(driver, selenium_actions, login_details, form_input_data)

        is_apply_account_successful = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'accountId'))
            ).text != '0'
        
        if is_apply_account_successful:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='screenshot on success')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='screenshot on failure')

        driver.quit()
        assert is_apply_account_successful, "Apply Account Failed"

        # try:
        #     WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'accountId')))
        # except TimeoutException:
        #     selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
        #         image_description='application failed')
        #     assert False
        # else:
        #     if driver.find_element(By.ID, "accountId").text == '0':
        #         assert False
        #         selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
        #         image_description='application failed')
        #     else:
        #         assert True
        #         selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
        #         image_description='screenshot on success')
        # driver.quit()

    @pytest.mark.parametrize("form_input_data", Form.generate_test_type_of_account())
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_type_of_account(self, driver, os_system, login_details, form_input_data):
        selenium_actions = SeleniumActions(driver)
        
        self.common_steps(driver, selenium_actions, login_details, form_input_data)

        is_apply_account_successful =  WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'accountId'))
            ).text != '0'

        if is_apply_account_successful:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='screenshot on failure')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='screenshot on success')

        driver.quit()
        assert not is_apply_account_successful
