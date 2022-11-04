import pytest
import platform

def main():
    N_JOBS = 5

    os_browser = {
        'windows': ['chrome', 'firefox'],
        'linux': ['chrome', 'firefox'],
        'macos': ['chrome', 'firefox'],
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

    for browser in os_browser[current_os]:
        retcode = pytest.main(['test_cases/', f'--browser={browser}', f'--os={current_os}', f'-n {N_JOBS}'])

if __name__ == '__main__':
    main()
