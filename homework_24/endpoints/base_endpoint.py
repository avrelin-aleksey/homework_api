import requests
import allure
import dotenv
import os
import json
from faker import Faker


dotenv.load_dotenv()
BASE_URL = os.getenv("BASE_URL")
HEADERS = json.loads(os.getenv("HEADERS"))
USER_NAME = os.getenv("USER_NAME")


fake = Faker()

memes_data = {
    "text": fake.sentence(),
    "url": fake.image_url(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
memes_data_post_id = {
    "id": 22,
    "text": fake.sentence(),
    "url": fake.image_url(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
memes_data_negative1 = {
    "text": fake.sentence(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
memes_data_negative2 = {
    "url": fake.image_url(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
memes_data_negative3 = {
    "info": {"key": fake.uuid4()},
}
memes_data_negative4 = {
    "tags": [fake.word() for _ in range(3)],
}
memes_data_negative5 = {
    "id": 22,
    "text": fake.sentence(),
    "url": fake.image_url(),
}
empty_value = {
    "text": "",
    "url": "",
    "tags": [],
    "info": {}
}
long_text = {
    "text": "ЫЫВы" * 1000,
    "url": fake.image_url(),
    "tags": [fake.word() for _ in range(3)],
    "info": {"key": fake.uuid4()},
}
invalid_tags = {
    "text": fake.sentence(),
    "url": fake.image_url(),
    "tags": "не валидный",
    "info": {"key": fake.uuid4()},
}


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
