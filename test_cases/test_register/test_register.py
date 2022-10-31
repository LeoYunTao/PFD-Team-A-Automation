import pytest
from selenium import webdriver
import os
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def test_register():

    form_input_data = {
        'firstName': ['Hello world'],
        'title': ['ms'],
        'middleName': ['ok'],
        'lastName': ['yes'],
        'gender': ['female'],
        'employmentStatus': ['Full-time'],
        'age': ['12/01/2001'],
        'maritalStatus': ['Single'],
        'numberOfDependents': [10],
        'username': ['cool'],
        'email': ['abc1234567@gmail.com'],
        'password': ['abc123']
    }

    chrome_file_path = os.path.abspath('../../drivers/windows/Chrome')
    
    options = Options()
    options.binary_location = os.path.join(chrome_file_path, "chrome.exe")
    
    driver = webdriver.Chrome(options=options, service=Service(os.path.join(chrome_file_path, "chromedriver.exe")))

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
                Select(form_field).select_by_value(value_to_enter)

        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        time.sleep(10)
