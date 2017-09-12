import pytest
import yaml


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="MobiV2",
        help="provide which API to test: MobiV2 or WAPI")

@pytest.fixture(scope='session')
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope='session')
def env_url(env):
	config = yaml.load(open('config.yml'))
	return config['ENV'][env.upper()]
   