import requests
import random
import allure

from config import URL, ENDPOINT, ERROR


class TestCreateOrders:

    @allure.title('Проверка создания заказа с ингредиентами авторизованным пользователем')
    def test_create_order_with_ingredient_user_authorized(self, login_user):
        response_ingredient = requests.get(f"{URL}{ENDPOINT.INGREDIENTS.value}")
        payload = {
                "ingredients": response_ingredient.json()["data"][0]['_id']
        }
        headers = {"Authorization": login_user}
        response = requests.post(f"{URL}{ENDPOINT.ORDERS.value}", headers=headers, data=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["order"]["ingredients"][0]["_id"] == response_ingredient.json()["data"][0]['_id']

    @allure.title('Проверка создания заказа с ингредиентами не авторизованным пользователем')
    def test_create_order_with_ingredient_user_not_authorized(self, login_user):
        response_ingredient = requests.get(f"{URL}{ENDPOINT.INGREDIENTS.value}")
        payload = {
                "ingredients": response_ingredient.json()["data"][0]['_id']

        }
        response = requests.post(f"{URL}{ENDPOINT.ORDERS.value}",  data=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title('Проверка создания заказа без ингредиентов не авторизованным пользователем')
    def test_create_order_not_ingredient_user_authorized(self, login_user):
        payload = {
                "ingredients": []

        }
        response = requests.post(f"{URL}{ENDPOINT.ORDERS.value}",  data=payload)
        assert response.status_code == 400
        assert response.json()["message"] == ERROR.INGREDIENT_MUST_BE_PROVIDED.value

    @allure.title('Проверка создания заказа с невалидным хешем ингредиентов')
    def test_create_order_hash_invalid(self, login_user):
        payload = {
                "ingredients": ["hash_error"]

        }
        response = requests.post(f"{URL}{ENDPOINT.ORDERS.value}",  data=payload)
        assert response.status_code == 500


class TestReceivingUserOrders:

    @allure.title('Проверка получения списка заказов авторизованным пользователем')
    def test_receiving_user_orders(self, login_user):
        response_ingredient = requests.get(f"{URL}{ENDPOINT.INGREDIENTS.value}")
        payload = {
                "ingredients": [response_ingredient.json()["data"][0]['_id'],
                                response_ingredient.json()["data"][1]['_id']]
        }
        headers = {"Authorization": login_user}
        requests.post(f"{URL}{ENDPOINT.ORDERS.value}", headers=headers, data=payload)
        response_receiving_user_orders = requests.get(f"{URL}{ENDPOINT.ORDERS.value}", headers=headers, data=payload)
        assert response_receiving_user_orders.status_code == 200
        assert response_receiving_user_orders.json()["success"] is True
        assert (response_ingredient.json()["data"][0]['_id'] ==
                response_receiving_user_orders.json()["orders"][0]['ingredients'][0])

    @allure.title('Проверка получения списка заказов неавторизованным пользователем')
    def test_receiving_user_orders(self, login_user):
        response_ingredient = requests.get(f"{URL}{ENDPOINT.INGREDIENTS.value}")
        payload = {
                "ingredients": [response_ingredient.json()["data"][0]['_id'],
                                response_ingredient.json()["data"][1]['_id']]
        }
        headers = {"Authorization": login_user}
        requests.post(f"{URL}{ENDPOINT.ORDERS.value}", headers=headers, data=payload)
        response_receiving_user_orders = requests.get(f"{URL}{ENDPOINT.ORDERS.value}", data=payload)
        assert response_receiving_user_orders.status_code == 401
        assert response_receiving_user_orders.json()["message"] == ERROR.USER_NOT_AUTHORIZED.value




