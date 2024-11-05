import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--endpoint", action="store",default='http://localhost:8080',help="API endpoint URL for prediction"
    )
    
@pytest.fixture
def endpoint(request):
    return request.config.getoption('--endpoint')