import string
from math import exp
import pytest
import time
import allure
import selenium
import platform
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidElementStateException

from selenium_actions import *


#import selenium_actions
#from selenium_actions import SeleniumActions


class TestForgotPassword:
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_find_email(self, driver, os_system):
        # log in credentials

        selenium_actions = SeleniumActions(driver)

        email = "terrence_eng@hotmail.com"  # THIS IS MY PERSONAL EMAIL DONT SPAM ME, currently hard coded

        selenium_actions.load_page("https://uibank.uipath.com/password-request", By.TAG_NAME, 'input')

        # find email field and send the username itself to the input field
        driver.find_element(By.ID, "email").send_keys(email)

        # click login button
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # Validate the email to check for error message

        # try:
        #     WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[class="text-center"')))
        #     #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="col-12 text-center"')))
        # except (TimeoutException) as error:
        #     assert True
        # else:
        #     try:
        #         WebDriverWait(driver, 10).until(
        #             EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="col-12 text-center"')))
        #     except (TimeoutException) as error:
        #         assert False
        #         print(error)
        #     finally:
        #         # close the driver
        #         driver.quit()

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'img.text-center')))
        except TimeoutException:
            assert False
        else:
            assert True
        finally:
            driver.quit()

        selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png',
                                           image_description='Screenshot on failure')
        driver.quit()
        #assert False, f"Email validation failed: {email['email']}"

# pytest test_cases/test_forgotPassword/ --alluredir=allure-report
