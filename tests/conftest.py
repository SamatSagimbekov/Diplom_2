import pytest
import requests
from config import URL, ENDPOINT
from helpers import get_payload_user
import json


@pytest.fixture
def create_user():
    login_pass = []
    payload = get_payload_user()
    response = requests.post(f"{URL}{ENDPOINT.CREATE_USER.value}", data=payload)
    if response.status_code == 200:
        login_pass.append(payload["email"])
        login_pass.append(payload["password"])
        login_pass.append(payload["name"])
    return {'response': response, 'login_pass': login_pass}


@pytest.fixture
def login_user(create_user):
    payload = {
        "email": create_user['login_pass'][0],
        "password": create_user['login_pass'][1],
    }
    response_login = requests.post(f"{URL}{ENDPOINT.LOGIN.value}", data=payload)
    return response_login.json()["accessToken"]

