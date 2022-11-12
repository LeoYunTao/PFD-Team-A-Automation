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

    #pytest test_cases/ -s -n 5 --csv testswindows.csv --csv-columns id, function, status, duration, message, parameters_as_columns
    #allure generate allure-results/* --clean
    #allure open allure-report/

    # allure-results -> allure-report

    retcode = pytest.main(['test_cases/', '--production=true', 
        f'-n {N_JOBS}', f'--alluredir=allure-results/{current_os}/',
        f'csv csv-reports/test_{current_os}.csv --csv-columns id, function, status, duration, message, parameters_as_columns'])
    #pytest test_cases/ -s -n 5 --csv csv-reports/testswindows.csv --csv-columns id, function, status, duration, message, parameters_as_columns

if __name__ == '__main__':
    main()
