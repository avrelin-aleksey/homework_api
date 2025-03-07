import allure
import pytest
from endpoints.test_config import (
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
        with allure.step("Проверка статус код 200"):
            memes_endpoint.check_status_code(200)
        with allure.step("Полученный id соответствует id при создании"):
            assert response["id"] == create_memes_for_test

    @allure.story("Получение мема с несуществующим id")
    def test_get_memes_invalid_id(self, memes_endpoint, token):
        memes_endpoint.get_memes_by_id(99999999, token)
        with allure.step("Проверка статус код = 404"):
            memes_endpoint.check_status_code(404)
        with allure.step("Приходит в ответе текст '404 Not Found'"):
            assert "404 Not Found" in memes_endpoint.response.text

    @allure.story("Получение всех мемов без авторизации по токену")
    def test_get_all_memes_without_auth(self, memes_endpoint):
        memes_endpoint.get_all_memes(None)
        with allure.step("Проверка статус код = 401"):
            memes_endpoint.check_status_code(401)
        with allure.step("Приходит в ответе текст '401 Unauthorized'"):
            assert "401 Unauthorized" in memes_endpoint.response.text

    import allure

    @allure.story("Получение всех мемов c авторизацией по токену")
    def test_get_memes_all(self, memes_endpoint, token):
        memes = memes_endpoint.get_all_memes(token)
        with allure.step("Проверка статус код = 200"):
            memes_endpoint.check_status_code(200)
        with allure.step("Проверка, что список мемов не пуст"):
            assert len(memes) > 0, "Список мемов пуст"
        with allure.step("Проверка, что в ответе присутствует ключ 'data'"):
            assert "data" in memes, "Ответ не содержит ключ 'data'"
        with allure.step("Проверка, что количество мемов больше 0"):
            memes_all_count = len(memes["data"])
            assert memes_all_count >= 1, (f"Ожидалось, что мемов в списке будет не меньше 1,"
                                         f" а список пуст и количество равно {memes_all_count}")


@allure.feature("Создание мемов")
class TestCreateMemes:
    @allure.story("Успешное создание мема")
    def test_create_memes(self, memes_endpoint, token):
        response = memes_endpoint.create_memes(token, **memes_data)
        with allure.step("Проверка статус код = 200"):
            memes_endpoint.check_status_code(200)
        with allure.step("Проверка наличия id"):
            assert response["id"] is not None
        with allure.step("Сравнение отправленного тела запроса и получаемого"):
            response_for_comparison = dict(filter(lambda x: x[0] in memes_data, response.items()))
            assert response_for_comparison == memes_data


    @allure.story("Создание мема без авторизации")
    def test_create_memes_without_auth(self, memes_endpoint):
        memes_endpoint.create_memes(None, **memes_data)
        with allure.step("Проверка статус код = 401"):
            memes_endpoint.check_status_code(401)
        with allure.step("Приходит в ответе текст '401 Unauthorized'"):
            assert "401 Unauthorized" in memes_endpoint.response.text

    @allure.story("Создание мема с пустыми значениями полей")
    def test_create_memes_empty_fields(self, memes_endpoint, token):
        memes_endpoint.create_memes(token, **empty_value)
        with allure.step("Проверка статус код = 400"):
            memes_endpoint.check_status_code(400) # приходит 200, но поидее должна быть ошибка
        with allure.step("Приходит в ответе текст 'Bad Request'"):
            assert "Bad Request" in memes_endpoint.response.text


    @allure.story("Отправка post-запроса с существующим id")
    def test_create_memes_with_existing_id(self, memes_endpoint, token):
        response = memes_endpoint.create_memes(token, **memes_data_post_id)
        with allure.step("Проверка статус код = 200"):
            memes_endpoint.check_status_code(200)
        with allure.step("Проверка наличия id"):
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
        with allure.step("Проверка статус код = 400"):
            memes_endpoint.check_status_code(400)
        with allure.step("Приходит в ответе текст 'Bad Request'"):
            assert "Bad Request" in memes_endpoint.response.text

    @allure.story("Создание мема с слишком длинным текстом")
    def test_create_memes_long_text(self, memes_endpoint, token):
        memes_endpoint.create_memes(token, **long_text)
        with allure.step("Проверка статус код = 200"):
            memes_endpoint.check_status_code(200) # тут не понятно должно ли быть 400 или 200

    @allure.story("Создание мема с невалидным tags")
    def test_create_memes_invalid_tags(self, memes_endpoint, token):
        memes_endpoint.create_memes(token, **invalid_tags)
        with allure.step("Проверка статус код = 400"):
            memes_endpoint.check_status_code(400)
        with allure.step("Приходит в ответе текст 'Bad Request'"):
            assert "Bad Request" in memes_endpoint.response.text


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
        with allure.step("Проверка статус код = 200"):
            memes_endpoint.check_status_code(200)
        with allure.step("Сравнение отправленного и полученного 'id'"):
            assert response["id"] == f"{create_memes_for_test}"
        with allure.step("Сравнение отправленного и полученного 'text'"):
            assert response["text"] == "Updated Meme"
        with allure.step("Сравнение отправленного и полученного 'url'"):
            assert response["url"] == "https://alekseys.mem/updated_memes.jpg"
        with allure.step("Сравнение отправленного и полученного 'tags'"):
            assert response["tags"] == ["updated", "test2"]
        with allure.step("Сравнение отправленного и полученного 'info'"):
            assert response["info"] == {"key": "updated_value"}

    @allure.story("PUT изменение мема с невалидными данными")
    @pytest.mark.parametrize('test_case', [
        memes_data_negative1,
        memes_data_negative2,
        memes_data_negative3,
        memes_data_negative4,
        memes_data_negative5])
    def test_update_memes_negative(self, memes_endpoint, token, create_memes_for_test, test_case):
        memes_endpoint.update_memes(create_memes_for_test, token, **test_case)
        with allure.step("Проверка статус код = 400"):
            memes_endpoint.check_status_code(400)
        with allure.step("Приходит в ответе текст 'Bad Request'"):
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
        with allure.step("Проверка статус код = 401"):
            memes_endpoint.check_status_code(401)
        with allure.step("Приходит в ответе текст '401 Unauthorized'"):
            assert "401 Unauthorized" in memes_endpoint.response.text


@allure.feature("Удаление мемов")
class TestDeleteMemes:
    @allure.story("Удаление существующего мема")
    def test_delete_memes(self, memes_endpoint, token, create_memes_for_test):
        memes_endpoint.delete_memes(create_memes_for_test, token)
        with allure.step("Удаление мема статус код = 200"):
            memes_endpoint.check_status_code(200)
        with allure.step("Проверка успешного удаления статус код = 404"):
            memes_endpoint.get_memes_by_id(create_memes_for_test, token)
            memes_endpoint.check_status_code(404)


    @allure.story("Удаление несуществующего мема")
    def test_delete_memes_negative(self, memes_endpoint, token):
        memes_endpoint.delete_memes(111111111111111111, token)
        with allure.step("Проверка статус код = 404"):
            memes_endpoint.check_status_code(404)
        with allure.step("Приходит в ответе текст '404 Not Found'"):
            assert "404 Not Found" in memes_endpoint.response.text

    @allure.story("Удаление мема дважды подряд")
    def test_delete_memes_twice(self, memes_endpoint, token, create_memes_for_test):
        with allure.step("Первая попытка удаления успешная"):
            memes_endpoint.delete_memes(create_memes_for_test, token)
        with allure.step("Вторая попытка удаления, не успешная"):
            memes_endpoint.delete_memes(create_memes_for_test, token)
        with allure.step("Проверка статус код = 404"):
            memes_endpoint.check_status_code(404)
        with allure.step("Приходит в ответе текст '404 Not Found'"):
            assert "404 Not Found" in memes_endpoint.response.text

    @allure.story("Удаление существующего мема без токена")
    def test_delete_memes_without_token(self, memes_endpoint, create_memes_for_test):
        memes_endpoint.delete_memes_without_token(create_memes_for_test)
        with allure.step("Проверка статус код = 400"):
            memes_endpoint.check_status_code(400) # но приходит ответ 200
        with allure.step("Приходит в ответе текст 'Bad Request'"):
            assert "Bad Request" in memes_endpoint.response.text
