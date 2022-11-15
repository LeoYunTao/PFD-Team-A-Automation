import allure

import os
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class SeleniumActions():

    def __init__(self, driver) -> None:
        self.driver = driver

    @allure.step
    def load_page(self, url, locator_strategy, locator_value):
        '''
        Loads the page and check that if an element exists on the page before proceeding
        '''

        self.driver.get(url)

        if self.is_element_located(locator_strategy, locator_value):
            self.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
                image_description='Screenshot on page load')
        else: 
            assert False, "Page failed to load"

    def is_element_located(self, locator_strategy, locator_value):
        '''
        Returns true if the element is found
        '''

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((locator_strategy, locator_value))
            )
        except:
            return False
        else:
            return True

    def is_alert_present(self):
        try: 
            WebDriverWait(self.driver, 5).until(
                EC.alert_is_present()
            )
        except:
            return False
        else:
            return True

    def upload_screenshot(self, tmp_file_path, image_description):
        '''Uploads the screenshot to allure'''

        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.screenshot(tmp_file_path)
        allure.attach.file(tmp_file_path, image_description, attachment_type=allure.attachment_type.PNG)
        os.remove(tmp_file_path)

    @allure.step
    def fill_form(self, form_input):
        '''
        Selects all the elements on the page with input and select tag.
        Next through all the element and key in the value.
        Submit after filling through all the values

        form_input - a dictionary where the key must contain the *name of the input tag*
        '''

        form_fields = self.driver.find_elements(By.CSS_SELECTOR, 'input, select')

        for form_field in form_fields:
            if form_field.get_attribute('name') not in form_input:
                continue
            value_to_enter = form_input[form_field.get_attribute('name')]

            self.enter_input(form_field, value_to_enter)

        self.upload_screenshot(tmp_file_path=f'{random.random()}.png', 
            image_description='Screenshot on form fill')

        self.submit_form()

    @allure.step
    def enter_input(self, form_field, value_to_enter):
        if form_field.tag_name == 'input':
            form_field.send_keys(str(value_to_enter))
        else:
            Select(form_field).select_by_index(value_to_enter)

    @allure.step
    def submit_form(self, custom_xpath=None):
        submit_button = None
        
        if custom_xpath == None:
            submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit" or @data-toggle="modal"]')
        else:
            submit_button = self.driver.find_element(By.XPATH, custom_xpath)
        
        submit_button.click()
