import os
import platform

current_os = platform.system()
if current_os == "Windows":
    os.system('powershell -command "irm get.scoop.sh | iex"')
    os.system('scoop install allure')
elif current_os == "Linux":
    os.system('sudo apt-add-repository ppa:qameta/allure')
    os.system('sudo apt-get update')
    os.system('sudo apt-get install allure')
elif current_os == "Darwin":
    os.system('brew install allure')
else:
    raise Exception("OS not found")

os.system('allure generate allure-results/* --clean')

