import pytest

from faker import Faker

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestApplyLoan:
    def test_applyloan(self, driver):
        # log in credentials
        email = "Terrence_eng@hotmail.com"
        amount = 100000
        term = 1
        income = 200000
        age = 18

        # head to uibank login page
        driver.get("https://uibank.uipath.com/loans/apply")
        # find username/email field and send the username itself to the input field
        driver.find_element(By.ID, "email").send_keys(email)
        # find password input field and insert password as well
        driver.find_element(By.ID, "amount").send_keys(amount)
        driver.find_element(By.ID, "term").send_keys(term)
        driver.find_element(By.ID, "income").send_keys(income)
        driver.find_element(By.ID, "age").send_keys(age)

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
