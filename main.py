import pytest
import platform
import os

from config import allure_results_path, csv_reports_path

def main():
    N_JOBS = 16

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

    REPEAT = 5

    os.environ['repeat'] = str(REPEAT)

    #pytest test_cases/ -s -n 5 --csv testswindows.csv --csv-columns id, function, status, duration, message, parameters_as_columns
    #allure generate allure-results/* --clean
    #allure open allure-report/

    # allure-results -> allure-report

    retcode = pytest.main(['test_cases/', '--production=true', 
        f'-nlogical', f'--alluredir={allure_results_path}/{current_os}/',
        f'--csv={csv_reports_path}/test_{current_os}.csv', '--csv-columns=id, function, status, duration, message, parameters_as_columns'])
    #pytest test_cases/ -s -n 5 --csv csv-reports/testswindows.csv --csv-columns id, function, status, duration, message, parameters_as_columns

if __name__ == '__main__':
    main()
