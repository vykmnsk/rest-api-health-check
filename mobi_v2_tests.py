import pytest
import yaml
import requests


config = yaml.load(open('config.yml'))
mobi_v2 = config['MOBI_V2']
req_headers = {"Content-Type": "application/json"}
req_data = '{}'
resp_content_types_expected = ['application/json', 'text/json; charset=UTF-8']

@pytest.fixture(scope='module')
def api_url():
	return mobi_v2['api_url']

@pytest.mark.parametrize("endpoint", mobi_v2['get_endpoints']['smoke'])
def test_get_smoke(env_url, api_url, endpoint):
	resp = requests.get(env_url + api_url + endpoint)
	verify_response(resp)

@pytest.mark.parametrize("endpoint", mobi_v2['get_endpoints']['all'])
def test_get_all(env_url, api_url, endpoint):
	resp = requests.get(env_url + api_url + endpoint)
	verify_response(resp)

@pytest.mark.parametrize("endpoint", mobi_v2['post_endpoints']['smoke'])
def test_post_smoke(env_url, api_url, endpoint):
	resp = requests.post(env_url + api_url + endpoint, data=req_data, headers=req_headers)
	verify_response(resp)

@pytest.mark.parametrize("endpoint", mobi_v2['post_endpoints']['all'])
def test_post_all(env_url, api_url, endpoint):
	resp = requests.post(env_url + api_url + endpoint, data=req_data, headers=req_headers)
	verify_response(resp)

@pytest.mark.parametrize("endpoint", mobi_v2['put_endpoints']['smoke'])
def test_put_smoke(env_url, api_url, endpoint):
	resp = requests.put(env_url + api_url + endpoint, data=req_data, headers=req_headers)
	verify_response(resp)

@pytest.mark.parametrize("endpoint", mobi_v2['put_endpoints']['all'])
def test_put_all(env_url, api_url, endpoint):
	resp = requests.put(env_url + api_url + endpoint, data=req_data, headers=req_headers)
	verify_response(resp)

def verify_response(resp):
	assert 200 <= resp.status_code <= 300
	assert resp.headers['Content-Type'] in resp_content_types_expected
	assert resp.content	