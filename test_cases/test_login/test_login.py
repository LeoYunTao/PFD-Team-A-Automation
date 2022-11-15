import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.firefox.FirefoxDriver;

class TestApplyLoan:
    def test_login(self, driver):
        # log in credentials
        username = "Terrence"
        password = "T049111F"

        # head to github login page
        driver.get("https://uibank.uipath.com/login")
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
