import pytest

import platform
import pandas as pd
import random

from config import URL
from selenium_actions import *

import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class TestTransferFundsData:
    @staticmethod
    def get_login_details():
        return pd.DataFrame({
            'username': ['yt'],
            'password': ['abc123'],
            
        }).to_dict('records')

    @staticmethod
    def get_transfer_money_form():
        return pd.DataFrame({
            'fromAccount': [0],
            'toAccount': [1],
            'amount': [f'{random.uniform(0, 100):.2f}']
        }).to_dict('records')

    @staticmethod
    def get_test_amount():
        return pd.DataFrame({
            'fromAccount': [0],
            'toAccount': [1],
            'amount': [f'{random.uniform(-10000, 0):.2f}']
        }).to_dict('records')

class TestTransferFunds:

    def common_steps(self, selenium_actions, driver, login_details):
        selenium_actions.load_page(URL['login'], By.TAG_NAME, 'input')

        selenium_actions.fill_form(login_details)

        selenium_actions.is_element_located(By.XPATH, '//h3[text()="Welcome!"]')
        assert 'https://uibank.uipath.com/accounts' == driver.current_url

        driver.find_element(By.XPATH, '//a[@href="/transfer-money"]').click()

        selenium_actions.is_element_located(By.XPATH, '//h3[text()="Transfer Money"]')
        assert 'https://uibank.uipath.com/transfer-money' == driver.current_url

    @pytest.mark.parametrize("login_details", TestTransferFundsData.get_login_details())
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_main(self, os_system, driver, login_details):
        selenium_actions = SeleniumActions(driver)

        self.common_steps(selenium_actions, driver, login_details)

        selenium_actions.fill_form(
            TestTransferFundsData.get_transfer_money_form()[0])

        time.sleep(1)

        selenium_actions.submit_form(custom_xpath='//button[text()="Confirm Transfer"]')

        if selenium_actions.is_element_located(By.XPATH, '//h1[text()="Your transfer was successful!"]'):
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                image_description='Screenshot on success')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                image_description='Screenshot on failure')
        
        assert 'https://uibank.uipath.com/transfer-result' == driver.current_url

        driver.quit()

    @pytest.mark.parametrize("login_details", TestTransferFundsData.get_login_details())
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_amount(self, os_system, driver, login_details):
        selenium_actions = SeleniumActions(driver)

        self.common_steps(selenium_actions, driver, login_details)

        selenium_actions.fill_form(
            TestTransferFundsData.get_test_amount()[0])

        time.sleep(1)

        selenium_actions.submit_form(custom_xpath='//button[text()="Confirm Transfer"]')

        if selenium_actions.is_element_located(By.XPATH, '//h1[text()="Your transfer was successful!"]'):
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                image_description='Screenshot on failure')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                image_description='Screenshot on success')
        
        assert 'https://uibank.uipath.com/transfer-result' != driver.current_url

        driver.quit()

