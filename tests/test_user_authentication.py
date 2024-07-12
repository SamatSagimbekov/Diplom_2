import requests
from config import URL, ENDPOINT, ERROR
from helpers import get_payload_user
import allure


class TestCreateUser:

    @allure.title('Проверка создания пользователя')
    def test_create_user(self):
        payload = get_payload_user()
        response = requests.post(f"{URL}{ENDPOINT.CREATE_USER.value}", data=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert (response.json()["user"]["email"] == payload["email"] and
                response.json()["user"]["name"] == payload["name"])

    @allure.title('Проверка создания пользователя с уже используещимся логином')
    def test_create_user_login_exists(self, create_user):
        payload = {
            "email":  create_user['login_pass'][0],
            "password": create_user['login_pass'][1],
            "name": create_user['login_pass'][2]
        }
        response = requests.post(f"{URL}{ENDPOINT.CREATE_USER.value}", data=payload)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR.USER_EXIST.value

    @allure.title('Проверка создания пользователя с пердачей не всех данных')
    def test_create_courier_missing_parameter(self):
        payload = {
            "password": "password",
            "name": "Username"
        }
        response = requests.post(f"{URL}{ENDPOINT.CREATE_USER.value}", data=payload)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR.MISSING_PARAMETER.value


class TestLoginUser:

    @allure.title('Проверка авторизации пользователем')
    def test_login_user(self, create_user):
        payload = {
            "email":  create_user['login_pass'][0],
            "password": create_user['login_pass'][1],
        }
        response = requests.post(f"{URL}{ENDPOINT.LOGIN.value}", data=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert (response.json()["user"]["email"] == payload["email"] and
                response.json()["user"]["name"] == create_user['login_pass'][2])
        assert isinstance(response.json()["accessToken"], str)

    @allure.title('Проверка авторизации пользователем с неверным паролем')
    def test_login_user_incorrect_password(self, create_user):
        payload = {
            "email":  create_user['login_pass'][0],
            "password": "error",
        }
        response = requests.post(f"{URL}{ENDPOINT.LOGIN.value}", data=payload)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR.INCORRECT_AUTHORIZATION_DATA.value

    @allure.title('Проверка авторизации пользователем с неверным логином')
    def test_login_user_incorrect_email(self, create_user):
        payload = {
            "email":  "error",
            "password": create_user['login_pass'][1],
        }
        response = requests.post(f"{URL}{ENDPOINT.LOGIN.value}", data=payload)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR.INCORRECT_AUTHORIZATION_DATA.value


class TestChangingUserData:

    @allure.title('Проверка изменения данных авторизованного пользователя')
    def test_user_changing_email(self, login_user):
        email_changing = get_payload_user()["email"]
        name_changing = get_payload_user()["name"]
        payload = {
            "email": email_changing,
            "name": name_changing,
        }
        headers = {"Authorization": login_user}
        response = requests.patch(f"{URL}{ENDPOINT.User.value}", headers=headers, data=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert (response.json()["user"]["email"] == email_changing and
                response.json()["user"]["name"] == name_changing)

    @allure.title('Проверка изменения данных неавторизованного пользователя')
    def test_user_changing_email_user_not_authorized(self, login_user):
        email_changing = get_payload_user()["email"]
        name_changing = get_payload_user()["name"]
        payload = {
            "email": email_changing,
            "name": name_changing,
        }
        response = requests.patch(f"{URL}{ENDPOINT.User.value}", data=payload)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR.USER_NOT_AUTHORIZED.value



