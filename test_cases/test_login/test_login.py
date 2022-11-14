import pytest
from logging import error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import chrome
from selenium.common.exceptions import NoSuchElementException

# log in credentials
username = "Terrence"
password = "T0491211F"

abc = 123

# initialize the Chrome driver
service = chrome.Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# head to github login page
driver.get("https://uibank.uipath.com/login")
# find username/email field and send the username itself to the input field
driver.find_element(By.ID, "username").send_keys(username)
# find password input field and insert password as well
driver.find_element(By.ID, "password").send_keys(password)

# click login button
submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
submit_button.click()
# wait the ready state to be complete
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)


# error_message = "Incorrect username or password."
# get the errors (if there are)

def check_exists():
    try:
        driver.find_element(By.CSS_SELECTOR, 'div[style="color: red"]')
    except NoSuchElementException:
        return True
    return False


# print the errors optionally
# for e in errors:
#     print(e.text)
# if we find that error message within errors, then login is failed
# if any(error_message in e.text for e in errors):
#    print("[!] Login failed")
# else:
#    print("[+] Login successful")

# close the driver
driver.quit()
