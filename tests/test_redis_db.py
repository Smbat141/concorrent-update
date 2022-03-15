from redis_db.redis import RedisDb

resource_initial_data = {b'ad_requests_count': b'0', b'impressions_requests_count': b'0'}
resource_normalized_data = {'ad_requests_count': 0, 'impressions_requests_count': 0}


# All functions take 'app' in order to flush db every time
def test_redis_db_get_or_create_dict_when_not_exist(app):
    resource_key = 'resource_name_2'
    new_data = {'ad_requests_count': 50, 'impressions_requests_count': 50}
    redis_db = RedisDb(resource_key)
    redis_db.create_dict_if_not_exist(new_data)
    resource_data = redis_db.get_dict()

    assert resource_data == new_data


def test_redis_db_get_or_create_dict_when_already_exist(app):
    resource_key = 'resource_name_3'
    new_data = {'ad_requests_count': 50, 'impressions_requests_count': 50}
    RedisDb(resource_key).redis.hset(resource_key, mapping=new_data)

    redis_db = RedisDb(resource_key)
    resource_data = redis_db.get_dict()

    assert resource_data == new_data


def test_redis_db_increment(app):
    resource_key = 'resource_name_4'
    new_data = {'ad_requests_count': 50, 'impressions_requests_count': 50}
    dict_after_increment = {'ad_requests_count': 55, 'impressions_requests_count': 55}

    redis_db = RedisDb(resource_key)
    redis_db.create_dict_if_not_exist(new_data)
    redis_db.increment_dict_value(resource_key, "ad_requests_count", 5)
    redis_db.increment_dict_value(resource_key, "impressions_requests_count", 5)

    resource_data = redis_db.get_dict()

    assert resource_data == dict_after_increment


def test_redis_db_dict_key_values_to_string_or_int(app):
    resource_key = 'resource_name_4'
    redis_db = RedisDb(resource_key)
    normalized_dict = redis_db.dict_key_values_to_string_or_int(resource_initial_data)

    assert normalized_dict == resource_normalized_data


def test_redis_db_normalize_byte(app):
    resource_key = 'resource_name_5'
    redis_db = RedisDb(resource_key)
    normalized_dict = redis_db.normalize_byte(b"Test")

    assert normalized_dict == "Test"
