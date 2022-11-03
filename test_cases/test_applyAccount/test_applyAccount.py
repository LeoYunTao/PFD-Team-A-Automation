import pytest

from faker import Faker

import random
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class TestApplyAccount:
    @pytest.fixture
    def form_input_data(self):
        return {
        'accountNickName' : [self.NickName()],
        'accountType' : [self.AccountType()]
    }

    def test_main(self, driver, form_input_data):
        for test_range in range(len(list(form_input_data())[0])):
            driver.get('https://uibank.uipath.com/accounts')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'input'))
        )

        form_fields = driver.find_elements(By.CSS_SELECTOR, 'input, select')

        for form_field in form_fields:
            if form_field.get_attribute('name') not in form_input_data:
                continue
        value_to_enter = form_input_data[form_field.get_attribute('name')][test_number]

        if form_field.tag_name == 'input':
            form_field.send_keys(value_to_enter)
        else:
            Select(form_field).select_by_index(value_to_enter)

    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_button.click()


