import pytest

from endpoints.memes import Memes
from endpoints.base_endpoint import Authorization
from endpoints.test_config import memes_data
from endpoints.base_endpoint import USER_NAME


@pytest.fixture(scope="session")
def auth_with_response():
    auth = Authorization()
    auth.authorization_user(USER_NAME)
    return auth


@pytest.fixture(scope="session")
def auth_with_response_without_name(scope="session"):
    auth = Authorization()
    auth.authorization_user('')
    return auth


@pytest.fixture(scope="session")
def token():
    authorization = Authorization()
    token = authorization.authorization_user(USER_NAME)
    yield token


@pytest.fixture
def memes_endpoint():
    return Memes()


@pytest.fixture
def create_memes_for_test(token, memes_endpoint):
    response = memes_endpoint.create_memes(token, **memes_data)
    meme_id = response["id"]
    yield meme_id
    memes_endpoint.delete_memes(meme_id, token)
