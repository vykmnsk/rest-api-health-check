import pytest
import yaml
import requests
import json

import random
import string

config = yaml.load(open('config.yml'))
wapi = config['WAPI']
JROOT = 'RSP'
json_content_types = [
    'application/json'
    , 'text/json; charset=utf-8'
    , 'application/json; charset=utf-8']

@pytest.fixture(scope='module')
def api_url():
    return wapi['api_url']

@pytest.fixture(scope='module')
def created_customer(env_url, api_url):
    req_data = {'action': 'account_insert_customer'}
    username = 'AutoApiUser' + rand_numeric(9)
    password = rand_alpha(7) + rand_numeric(3)
    telephone_password = rand_alpha(7) + rand_numeric(3)
    secret_answer = rand_alpha_numeric(10)
    cust_data = {
        'username': username,
        'lastname': rand_alpha_numeric(30),
        'password': password,
        'internet_password': password,
        'telephone_password': telephone_password,
        'email_address': username + '@example.com',
        'amlStatus': 'active_-_kyc_verified',
        'building': 'Level5',
        'city': 'Adelaide',
        'country': 'GB',
        'currency_code': 'GBP',
        'depositAmount': '100.00',
        'deposit_limit': 'N/A',
        'dob': '1942-09-06',
        'finalBalance': '80.00',
        'firstname': 'Oswald',
        'lastname': 'Petrucco',
        'manual_verification': 'Y',
        'postcode': '5006',
        'salutation': 'Mr',
        'secret_question': 'Favourite Holiday Spot?',
        'secret_answer': secret_answer,
        'state': 'N/A',
        'street': '142 Tynte Street',
        'suburb': 'N/A',
        'telephone': '0463254781',
        'timezone': 'N/A',
        'withrawAmount': '20.00',
        }
    req_data.update(wapi['credentials'])
    req_data.update(cust_data)
    jresp = jpost(env_url, api_url, req_data)
    verify_has_no_error(jresp)
    assert jresp['success']['message'] == 'Customer Created'
    return {'customer_username': username, 'customer_password': password}

@pytest.fixture(scope='module')
def valid_credentials(created_customer):
    return dict(wapi['credentials'], **created_customer)

@pytest.fixture(scope='module')
def invalid_credentials(valid_credentials):
    return dict(valid_credentials, **{'wapi_client_pass': 'bad password'})


def rand_alpha(size):
    return ''.join([random.choice(string.ascii_letters) for n in range(size)])  

def rand_numeric(size):
    return ''.join([random.choice(string.digits) for n in range(size)]) 

def rand_alpha_numeric(size):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)])  


def test_fail_no_action_provided(env_url, api_url):
    req_data = {}
    jresp = jpost(env_url, api_url, req_data)
    verify_has_error(jresp, 'No action provided')

def test_fail_autorization_incomplete(env_url, api_url):
    req_data = {'action': 'bet_get_balance'}
    jresp = jpost(env_url, api_url, req_data)
    verify_jresp_api(jresp, 'bet')
    verify_has_error(jresp)
    verify_has_error(jresp, 'Client authorisation is incomplete')

def test_fail_login(env_url, api_url, invalid_credentials):
    req_data = {'action': 'account_login'}
    req_data.update(invalid_credentials)
    jresp = jpost(env_url, api_url, req_data)
    verify_has_error(jresp, 'Invalid WAPI client user or password')

def test_login(env_url, api_url, valid_credentials):
    req_data = {'action': 'account_login'}
    req_data.update(valid_credentials)
    jresp = jpost(env_url, api_url, req_data)
    verify_has_no_error(jresp)
    verify_jresp_api(jresp, 'account')

def jpost(env_url, api_url, data):
    data.update({"output_type": "json"})
    print(f'\n<-- POST: {data}')
    resp = requests.post(env_url + api_url, data=data)
    print(f'\nResp: --> {resp.content}')
    return verify_parse_json(resp)

def verify_parse_json(resp):
    assert 200 <= resp.status_code <= 300
    assert resp.content
    return json.loads(resp.content)[JROOT]

def verify_jresp_api(jresp, api):
    assert jresp['api'] == api

def verify_has_no_error(jresp):
    err_keys = ('error', 'customer_errors')
    resp_keys = jresp.keys()
    for err_key in err_keys:
        assert err_key not in resp_keys

def verify_has_error(jresp, with_text=None):
    err_key = 'error'
    assert err_key in jresp.keys()
    if with_text:
        all_errors = jresp[err_key]
        assert any(with_text in err['error_text'] for err in all_errors), \
                f'{with_text} not in {all_errors}'

