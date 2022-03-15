import pytest
import os
from main import create_app
from redis_db.redis import RedisDb

os.environ['FLASK_ENV'] = 'testing'


@pytest.fixture()
def app():
    # clear test db for every test
    RedisDb('test').redis.flushdb()
    app = create_app()
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def query_params():
    return {
        'sdk_version': '1.0',
        'session_id': 'sdflskdhafksdfha',
        'platform': 'Linux',
        'username': 'user_1',
        'country_code': 'CA'
    }
