import pytest

def pytest_addoption(parser):
    parser.addoption(
        '--browser', action='store', 
        default='chrome', help='The browser to perform testing on'
    )
    parser.addoption(
        '--os', action='store', 
        default='windows', help='The os that the testing will be performed on'
    )

@pytest.fixture
def browser(request):
    return request.config.getoption('--browser')

@pytest.fixture
def os_system(request):
    return request.config.getoption('--os')