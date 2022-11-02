import pytest

from faker import Faker

import random
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class TestRegister:
    @pytest.fixture
    def form_input_data(self):
        rows = 10

        fake = Faker()
        return {
            'firstName': [fake.unique.first_name() for _ in range(rows)],
            'title': [random.randint(0, 2) for _ in range(rows)],
            'middleName': [fake.unique.first_name() for _ in range(rows)],
            'lastName': [fake.unique.last_name() for _ in range(rows)],
            'gender': [random.randint(0, 1) for _ in range(rows)],
            'employmentStatus': [random.randint(0, 2) for _ in range(rows)],
            'age': [fake.unique.date_of_birth().strftime("%m/%d/%Y") for _ in range(rows)],
            'maritalStatus': [random.randint(0, 3) for _ in range(rows)],
            'numberOfDependents': [random.randint(0, 100) for _ in range(rows)],
            'username': [fake.unique.user_name() for _ in range(rows)],
            'email': [fake.unique.email() for _ in range(rows)],
            'password': [fake.unique.password() for _ in range(rows)]
        }

    def test_main(self, driver, form_input_data):

        for test_number in range(len(list(form_input_data.values())[0])):

            driver.get('https://uibank.uipath.com/register-account')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'input'))
            )

            form_fields = driver.find_elements(By.CSS_SELECTOR , 'input, select')

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

            try: 
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//p[text()="Check your inbox for a verification link."]'))
                )
            except:
                driver.quit()
                assert False, "Registration Failed"

        driver.quit()
