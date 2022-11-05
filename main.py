import pytest
import platform

def main():
    N_JOBS = 5

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

    for browser in os_browser[current_os]:
        retcode = pytest.main(['test_cases/', f'--browser={browser}', f'-n {N_JOBS}', '--production=true', '-k "test_register"'])

if __name__ == '__main__':
    main()
