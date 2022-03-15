from typing import Union

import redis as r
import os
from dotenv import dotenv_values


class RedisDb:

    def __init__(self, name):

        config = dotenv_values('.env')

        if os.environ['FLASK_ENV'] == 'testing':
            host = config['TEST_REDIS_HOST']
            port = config['TEST_REDIS_PORT']
            db = config['TEST_REDIS_DB']
        else:
            host = config['REDIS_HOST']
            port = config['REDIS_PORT']
            db = config['REDIS_DB']

        self.name = name
        self.redis = r.Redis(host=host, port=port, db=db)

    def create_dict_if_not_exist(self, dct) -> dict:
        for key, value in dct.items():
            self.redis.hsetnx(self.name, key, value)
            self.redis.hsetnx(self.name, key, value)

    def get_dict(self):
        resource_data = self.dict_key_values_to_string_or_int(self.redis.hgetall(self.name))
        return resource_data

    def increment_dict_value(self, resource_key, increment_key, n):
        self.redis.hincrby(resource_key, increment_key, n)

    def dict_key_values_to_string_or_int(self, dct: dict) -> dict:
        converted_dict = {}
        for key, value in dct.items():
            key = self.normalize_byte(key)
            value = self.normalize_byte(value)
            converted_dict[key] = value

        return converted_dict

    def normalize_byte(self, byt: bytes) -> Union[int, str]:
        return int(byt.decode('ascii')) if byt.decode('ascii').isnumeric() else byt.decode('ascii')
