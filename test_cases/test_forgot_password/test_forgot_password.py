import pytest
import time
import pandas as pd
import platform
import random
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidElementStateException

from selenium_actions import *
from config import URL


#import selenium_actions
#from selenium_actions import SeleniumActions

class TestForgotPasswordData():

    @staticmethod
    def generate_test_email(rows=5):
        fake = Faker()
        return pd.DataFrame({
            'email': [fake.unique.email().split("@")[0] + str(random.random())[2:] + "@" + fake.unique.email().split("@")[1] for _ in range(rows)]
        }).to_dict('records')

class TestForgotPassword:

    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_main(self, driver, os_system, email):

        selenium_actions = SeleniumActions(driver)

        selenium_actions.load_page(URL['forgot_password'], By.TAG_NAME, 'input')

        selenium_actions.fill_form(email)

        is_email_reset_successful = selenium_actions.is_element_located(By.XPATH, '//h3[text()=" Your link to reset has been sent to your email! "]')

        if is_email_reset_successful:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                           image_description='Screenshot on success')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                           image_description='Screenshot on failure')

        assert is_email_reset_successful

    @pytest.mark.parametrize('form_input_data', TestForgotPasswordData.generate_test_email(rows=int(os.environ['repeat'])))
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_email(self, driver, os_system, form_input_data):

        selenium_actions = SeleniumActions(driver)

        selenium_actions.load_page(URL['forgot_password'], By.TAG_NAME, 'input')

        selenium_actions.fill_form(form_input_data)

        is_email_reset_successful = not selenium_actions.is_element_located(By.XPATH, '//div[text()=" There was an error "]')

        if is_email_reset_successful:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                           image_description='Screenshot on failure')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                image_description='Screenshot on success')

        assert not is_email_reset_successful

