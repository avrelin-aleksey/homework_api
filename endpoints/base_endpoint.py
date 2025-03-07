import requests
import allure
import dotenv
import os
import json


dotenv.load_dotenv()
BASE_URL = os.getenv("BASE_URL")
HEADERS = json.loads(os.getenv("HEADERS"))
USER_NAME = os.getenv("USER_NAME")


class BaseEndpoint:
    def __init__(self):
        self.url = BASE_URL
        self.headers = HEADERS
        self.response = None

    @allure.step("Проверка статус-кода")
    def check_status_code(self, code):
        assert self.response.status_code == code, f"Код ответа {self.response.status_code}"


class Authorization(BaseEndpoint):
    @allure.step("Создание пользователя")
    def authorization_user(self, name):
        self.response = requests.post(
            f"{self.url}/authorize",
            json={"name": name},
            headers=self.headers
        )
        self.token = self.response.json()["token"]
        return self.token
