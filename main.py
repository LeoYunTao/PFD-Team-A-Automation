import pytest
import platform
import os

def main():
    N_JOBS = 10

    os_browser = {
        'windows': ['chrome', 'firefox', 'edge'],
        'linux': ['chrome', 'firefox', 'edge'],
        'macos': ['chrome', 'firefox', 'edge'],
    }

    current_os = platform.system()
    if current_os == "Windows":
        current_os = current_os.lower()
    elif current_os == "Linux":
        current_os = current_os.lower()
    elif current_os == "Darwin":
        current_os = "macos"
    else:
        raise Exception("OS not found")

    os.environ['browsers'] = ','.join(os_browser[current_os])

    #allure generate allure-results/* --clean
    #allure open allure-report/

    # allure-results -> allure-report

    retcode = pytest.main(['test_cases/', '--production=true', f'-n {N_JOBS}', f'--alluredir=allure-results/{current_os}/'])#, f'--html=reports/report.html'])

if __name__ == '__main__':
    main()
