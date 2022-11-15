import pytest

from config import URL
from selenium_actions import *

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select


class TestApplyAccount:
    def test_applyAccount(self, driver):
        # log in credentials
        nickname = "test"

        selenium_actions = SeleniumActions(driver)
        selenium_actions.login()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[tabindex="0"]')))
        applyAccountPage = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"]')
        applyAccountPage.click()

        # find username/email field and send the username itself to the input field
        # driver.find_element(By.ID, "accountNickname").send_keys(nickname)
        # # find password input field and insert password as well
        # dropdown = Select(driver.find_element(By.ID, "typeOfAccount"))
        # dropdown.select_by_value('checking')

        # click apply button
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        # if selenium_actions.is_element_located(By.ID, "accountId"):
        #
        #     # check if the log in has failed by locating the log in error message
        #     if driver.find_element(By.ID, "accountId").text == '0':
        #         assert False
        #     else:
        #         assert True
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'accountId')))
        except TimeoutException:
            assert False
        else:
            if driver.find_element(By.ID, "accountId").text == '0':
                assert False
            else:
                assert True
        driver.quit()
