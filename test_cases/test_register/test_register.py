import pytest

from faker import Faker

import random
import pandas as pd
import platform
import csv

from config import URL
from selenium_actions import *

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
            'username': [fake.unique.user_name() + str(random.random())[2:] for _ in range(rows)],
            'email': [fake.unique.email().split("@")[0] + str(random.random())[2:] + "@" + fake.unique.email().split("@")[1] for _ in range(rows)],
            'password': [fake.unique.password() for _ in range(rows)]
        })

    @staticmethod
    def generate_test_main(rows=5):
        return TestRegisterData.generate_form_data(rows).to_dict('records')

    @staticmethod
    def generate_test_email():
        form_input_datas = TestRegisterData.generate_form_data(5)
        form_input_datas.email = pd.Series(['Zachy.aslam@gmail.com', '', 'abc123', None, 'test123.com'])
        return form_input_datas.to_dict('records')

class TestRegister:

    def common_steps(self, selenium_actions, form_input_data):
        selenium_actions.load_page(URL['register'], By.TAG_NAME, 'input')

        selenium_actions.fill_form(form_input_data)


    @pytest.mark.parametrize("form_input_data", TestRegisterData.generate_test_main(rows=5))
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_main(self, os_system, driver, form_input_data):

        fake = Faker()

        form_input_data['username'] = fake.unique.user_name() + str(random.random())[2:]
        form_input_data['email'] = fake.unique.email().split("@")[0] + str(random.random())[2:] + "@" + fake.unique.email().split("@")[1]

        selenium_actions = SeleniumActions(driver)

        self.common_steps(selenium_actions, form_input_data)

        if not selenium_actions.is_element_located(By.XPATH, '//p[text()="Check your inbox for a verification link."]'):
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                image_description='Screenshot on failure')
            driver.quit()
            assert False, "Registration Failed"
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                image_description='Screenshot on success')
        
        driver.quit()

    @pytest.mark.parametrize("form_input_data", TestRegisterData.generate_test_email())
    @pytest.mark.parametrize("os_system", [platform.platform()])
    def test_email(self, os_system, driver, form_input_data):

        if form_input_data['email'] == None:
            fake = Faker()
            form_input_data['email'] = fake.unique.email().split("@")[0] + str(random.random())[2:] + "@" + fake.unique.email().split("@")[1]
            form_input_data['email'] = form_input_data['email'].split('.')[0]

        selenium_actions = SeleniumActions(driver)
        
        self.common_steps(selenium_actions, form_input_data)

        is_alert_present = selenium_actions.is_alert_present()

        if is_alert_present:
            driver.switch_to.alert.dismiss()
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                image_description='Screenshot on success')
        else:
            selenium_actions.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                    image_description='Screenshot on failure')
        
        driver.quit()
        assert is_alert_present, f"Email validation failed: {form_input_data['email']}"

