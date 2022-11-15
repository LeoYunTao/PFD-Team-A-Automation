import string
from math import exp

import pytest
import time
import selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidElementStateException






class TestForgotPassword:
    def find_forgetPassword(self, driver):
        # log in credentials

        email = "s10204144@connect.np.edu.sg"  #THIS IS MY PERSONAL EMAIL DONT SPAM ME, currently hard coded

        # head to github login page
        driver.get("https://uibank.uipath.com/password-request")
        # find email field and send the username itself to the input field
        driver.find_element(By.ID, "email").send_keys(email)

        # click login button
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # Validate the email to check for error message

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.className, "col-12 text-center")))
        except (TimeoutException, InvalidElementStateException) as error:
            assert True
        else:
            assert False
        finally:
            # close the driver
            print(error)
            driver.quit()
#pytest test_cases/test_forgotPassword/