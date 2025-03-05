import allure


@allure.feature("Авторизация")
class TestAuthorization:
    @allure.story("Успешная авторизация пользователя")
    def test_authorization_user(self, auth_with_response):
        assert auth_with_response.response.status_code == 200, f"Код ответа {auth_with_response.response.status_code}"
        assert auth_with_response.token is not None

    @allure.story("Авторизация с пустым именем")
    def test_authorization_empty_name(self, auth_with_response_without_name):
        assert auth_with_response_without_name.response.status_code in [400, 401] # приходит 200
