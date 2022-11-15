import pytest

from config import URL
from selenium_actions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestLogIn:
    def login(self, driver, password):
        # log in credentials
        username = "Terrence"

        selenium_actions = SeleniumActions(driver)
        selenium_actions.load_page(URL['login'], By.TAG_NAME, 'input')
        # find username/email field and send the username itself to the input field
        driver.find_element(By.ID, "username").send_keys(username)
        # find password input field and insert password as well
        driver.find_element(By.ID, "password").send_keys(password)

        # click login button
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # check if the log in has failed by locating the log in error message
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[style="color: red"]')))
        except TimeoutException:
            assert True
        else:
            assert False
        finally:
            # close the driver
            driver.quit()

    def validPass(self):
        password = "T0491211F"
        return password

    def invalidPass(self):
        password = "S10223166"
        return password

    def test_loginTest(self, driver):
        password = self.invalidPass()
        self.login(driver, password)
