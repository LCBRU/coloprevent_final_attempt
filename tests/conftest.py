import pytest
from faker import Faker
from lbrc_flask.pytest.fixtures import *
from coloprevent import create_app
from lbrc_flask.pytest.faker import LbrcFlaskFakerProvider, UserProvider
from coloprevent.config import TestConfig
from tests.faker import ColoPreventProvider


@pytest.fixture(scope="function")
def standard_sites(client, faker):
    return faker.site().get_list_in_db(item_count=5)


@pytest.fixture(scope="function")
def standard_packtypes(client, faker):
    return faker.packtype().get_list_in_db(item_count=5)


@pytest.fixture(scope="function")
def app(tmp_path):
    class LocalTestConfig(TestConfig):
        FILE_UPLOAD_DIRECTORY = tmp_path

    yield create_app(LocalTestConfig)


@pytest.fixture(scope="function")
def faker():
    result: Faker = Faker("en_GB")
    result.add_provider(UserProvider)
    result.add_provider(LbrcFlaskFakerProvider)
    result.add_provider(ColoPreventProvider)

    yield result
