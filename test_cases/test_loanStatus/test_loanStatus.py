import pytest

from config import URL
from selenium_actions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestLogIn:
    def Status(self, driver, ID):
        # log in credentials

        selenium_actions = SeleniumActions(driver)
        selenium_actions.login()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="/loans/lookup"]')))
        LoanStatusPage = driver.find_element(By.XPATH, '//a[@href="/loans/lookup"]')
        LoanStatusPage.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'quoteID')))
        # find username/email field and send the username itself to the input field
        driver.find_element(By.ID, "quoteID").send_keys(ID)

        # click login button
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # check if the log in has failed by locating the log in error message
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, 'email')))
        except TimeoutException:
            assert False
        else:
            assert True
        finally:
            # close the driver
            driver.quit()

    def validId(self):
        ID = "637336a5929b090046800455"
        return ID

    def invalidId(self):
        ID = "wrongID"
        return ID

    def test_loanStatus(self, driver):
        ID = self.validId()
        self.Status(driver, ID)
