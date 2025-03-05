import allure
import pytest
from endpoints.base_endpoint import (
    memes_data_negative1,
    memes_data_negative2,
    memes_data_negative3,
    memes_data_negative4,
    memes_data_negative5,
    memes_data,
    memes_data_post_id,
    empty_value,
    long_text,
    invalid_tags
)


@allure.feature("Получение мемов")
class TestGetMemes:
    @allure.story("Получение мема по существующему id")
    def test_get_memes_by_id(self, memes_endpoint, token, create_memes_for_test):
        response = memes_endpoint.get_memes_by_id(create_memes_for_test, token)
        memes_endpoint.check_status_code(200)
        assert response["id"] == create_memes_for_test

    @allure.story("Получение мема с несуществующим id")
    def test_get_memes_invalid_id(self, memes_endpoint, token):
        memes_endpoint.get_memes_by_id(99999999, token)
        memes_endpoint.check_status_code(404)


@allure.feature("Создание мемов")
class TestCreateMemes:
    @allure.story("Успешное создание мема")
    def test_create_memes(self, memes_endpoint, token):
        response = memes_endpoint.create_memes(token, **memes_data)
        memes_endpoint.check_status_code(200)
        assert response["id"] is not None

    @allure.story("Создание мема без авторизации")
    def test_create_memes_without_auth(self, memes_endpoint):
        memes_endpoint.create_memes(None, **memes_data)
        memes_endpoint.check_status_code(401)

    @allure.story("Создание мема с пустыми значениями полей")
    def test_create_memes_empty_fields(self, memes_endpoint, token):
        memes_endpoint.create_memes(token, **empty_value)
        memes_endpoint.check_status_code(400) # приходит 200

    @allure.story("Отправка post-запроса с существующим id")
    def test_create_memes_with_existing_id(self, memes_endpoint, token):
        response = memes_endpoint.create_memes(token, **memes_data_post_id)
        memes_endpoint.check_status_code(200)
        assert response["id"] is not None

    @allure.story("Создание мема c невалидными body")
    @pytest.mark.parametrize('test_case', [
        memes_data_negative1,
        memes_data_negative2,
        memes_data_negative3,
        memes_data_negative4,
        memes_data_negative5])
    def test_create_memes_negative(self, memes_endpoint, token, test_case):
        memes_endpoint.create_memes(token, **test_case)
        memes_endpoint.check_status_code(400)

    @allure.story("Создание мема с слишком длинным текстом")
    def test_create_memes_long_text(self, memes_endpoint, token):
        memes_endpoint.create_memes(token, **long_text)
        memes_endpoint.check_status_code(200) # тут не понятно должно ли быть 400 или 200

    @allure.story("Создание мема с невалидным tags")
    def test_create_memes_invalid_tags(self, memes_endpoint, token):
        memes_endpoint.create_memes(token, **invalid_tags)
        memes_endpoint.check_status_code(400)


@allure.feature("Изменение мемов")
class TestUpdateMemes:
    @allure.story("PUT успешное изменение мема")
    def test_update_memes(self, memes_endpoint, token, create_memes_for_test):
        updated_data = {
            "id": create_memes_for_test,
            "text": "Updated Meme",
            "url": "https://alekseys.mem/updated_memes.jpg",
            "tags": ["updated", "test2"],
            "info": {"key": "updated_value"},
        }
        response = memes_endpoint.update_memes(create_memes_for_test, token, **updated_data)
        memes_endpoint.check_status_code(200)
        assert response["text"] == "Updated Meme"

    @allure.story("PUT изменение мема с невалидными данными")
    @pytest.mark.parametrize('test_case', [
        memes_data_negative1,
        memes_data_negative2,
        memes_data_negative3,
        memes_data_negative4,
        memes_data_negative5])
    def test_update_memes_negative(self, memes_endpoint, token, create_memes_for_test, test_case):
        memes_endpoint.update_memes(create_memes_for_test, token, **test_case)
        memes_endpoint.check_status_code(400)
        assert "Bad Request" in memes_endpoint.response.text

    @allure.story("Обновление мема без авторизации")
    def test_update_memes_without_auth(self, memes_endpoint, create_memes_for_test):
        updated_data = {
            "id": create_memes_for_test,
            "text": "Updated Meme",
            "url": "https://alekseys.mem/updated_memes.jpg",
            "tags": ["updated", "test2"],
            "info": {"key": "updated_value"},
        }
        memes_endpoint.update_memes(create_memes_for_test, token=None, **updated_data)
        memes_endpoint.check_status_code(401)


@allure.feature("Удаление мемов")
class TestDeleteMemes:
    @allure.story("Удаление существующего мема")
    def test_delete_memes(self, memes_endpoint, token, create_memes_for_test):
        memes_endpoint.delete_memes(create_memes_for_test, token)
        memes_endpoint.check_status_code(200)

    @allure.story("Удаление несуществующего мема")
    def test_delete_memes_negative(self, memes_endpoint, token):
        memes_endpoint.delete_memes(111111111111111111, token)
        memes_endpoint.check_status_code(404)

    @allure.story("Удаление мема дважды подряд")
    def test_delete_memes_twice(self, memes_endpoint, token, create_memes_for_test):
        memes_endpoint.delete_memes(create_memes_for_test, token)
        memes_endpoint.delete_memes(create_memes_for_test, token)
        memes_endpoint.check_status_code(404)

    @allure.story("Удаление существующего мема без токена")
    def test_delete_memes_without_token(self, memes_endpoint, create_memes_for_test):
        memes_endpoint.delete_memes_without_token(create_memes_for_test)
        memes_endpoint.check_status_code(400) # но приходит ответ 200
