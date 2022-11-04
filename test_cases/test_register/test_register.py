import pytest

from faker import Faker

import random
import pandas as pd

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class TestRegisterData:

    @staticmethod
    def generate_form_data(rows=5):
        fake = Faker()
        return pd.DataFrame({
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
            'email': [fake.unique.email().split("@")[0] + str(random.random())[2:] + "@" + fake.unique.email().split("@")[1] for _ in range(rows)],
            'password': [fake.unique.password() for _ in range(rows)]
        })

    @staticmethod
    def generate_test_main(rows=5):
        return TestRegisterData.generate_form_data(rows).to_dict('records')

    @staticmethod
    def generate_test_email(rows=5):
        form_input_datas = TestRegisterData.generate_form_data(rows)
        form_input_datas.email = pd.Series(['Zachy.aslam@gmail.com', '', 'abc123', form_input_datas.email.iloc[3].split('.')[0], 'test123.com'])
        return form_input_datas.to_dict('records')

class TestRegister:

    def fill_form(self, driver, form_input):
        driver.get('https://uibank.uipath.com/register-account')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'input'))
        )

        form_fields = driver.find_elements(By.CSS_SELECTOR , 'input, select')

        for form_field in form_fields:
            if form_field.get_attribute('name') not in form_input:
                continue
            value_to_enter = form_input[form_field.get_attribute('name')]

            if form_field.tag_name == 'input':
                form_field.send_keys(str(value_to_enter))
            else:
                Select(form_field).select_by_index(value_to_enter)

        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

    @pytest.mark.parametrize("form_input_data", TestRegisterData.generate_test_main(rows=5))
    def test_main(self, driver, form_input_data):

        self.fill_form(driver, form_input_data)

        try: 
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//p[text()="Check your inbox for a verification link."]'))
            )
        except:
            driver.quit()
            assert False, "Registration Failed"

        driver.quit()

    @pytest.mark.parametrize("form_input_data", TestRegisterData.generate_test_email(rows=5))
    def test_email(self, driver, form_input_data):

        self.fill_form(driver, form_input_data)

        try: 
            WebDriverWait(driver, 5).until(
                EC.alert_is_present()
            )
            driver.switch_to.alert.dismiss()
        except:
            driver.quit()
            assert False, f"Email validation failed: {form_input_data['email']}"


        driver.quit()
