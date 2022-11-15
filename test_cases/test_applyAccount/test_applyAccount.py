import pytest
import platform
import pandas as pd

from config import URL
from selenium_actions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

class Form:
    @staticmethod
    def login_details():
        return pd.DataFrame({
            'username': ["Terrence"],
            'password': ["T0491211F"],
        }).to_dict("records")

    @staticmethod
    def account_details():
        return pd.DataFrame({
            'accountNickname': ["Test"],
            'typeOfAccount': [0],
        }).to_dict("records")
class TestApplyAccount:
    @pytest.mark.parametrize("form_input_data", Form.login_details())
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_applyAccount(self, driver, os_system, form_input_data):

        selenium_actions = SeleniumActions(driver)
        selenium_actions.login(form_input_data)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[tabindex="0"]')))
        applyAccountPage = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"]')
        applyAccountPage.click()

        selenium_actions.fill_form(Form.account_details()[0])

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'accountId')))
        except TimeoutException:
            assert False
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='application failed')
        else:
            if driver.find_element(By.ID, "accountId").text == '0':
                assert False
                selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='application failed')
            else:
                assert True
                selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                image_description='screenshot on success')
        driver.quit()
