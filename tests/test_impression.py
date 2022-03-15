import json
from impression.impression import Impression
from redis_db.redis import RedisDb


def binary_to_json(binary):
    return json.loads(binary.decode('utf8'))


def dict_without_keys(dct, keys):
    return {key: dct[key] for key in dct if key not in keys}


def test_impression_get_without_permitted_params(client):
    failed_response = {'success': False,
                       'message': "following params are required ['sdk_version', 'session_id', 'platform', 'username', 'country_code']"}

    response = binary_to_json(client.get('/impression').data)
    assert response == failed_response


def test_impression_get_without_sdk_version(client, query_params):
    failed_response = {'success': False, 'message': "following params are required ['sdk_version']"}
    query_params_without_sdk_version = dict_without_keys(query_params, ['sdk_version'])
    response = binary_to_json(client.get('/impression', query_string=query_params_without_sdk_version).data)
    assert response == failed_response


def test_impression_get_without_username(client, query_params):
    failed_response = {'success': False,
                       'message': "following params are required ['username']"}

    query_params_without_username = dict_without_keys(query_params, ['username'])
    response = binary_to_json(client.get('/impression', query_string=query_params_without_username).data)

    assert response == failed_response


def test_impression_get_method_success(client, query_params, mocker):
    successful_response = {'success': True, 'message': "Successfully fetched"}
    # mock function for stats calculation and return simple message
    mocker.patch.object(Impression, 'calculate_user_and_sdk', return_value=True)

    response = binary_to_json(client.get('/impression', query_string=query_params).data)

    assert response == successful_response


def test_impression_calculate_user_and_sdk(app):
    resource_data_after_increment = {'impressions_requests_count': 2}
    with app.test_request_context():
        impression = Impression()
        username = "user_1"
        sdk_version = "1.0"
        impression.params = {"params": {"username": username, "sdk_version": sdk_version}}

        impression.calculate_user_and_sdk()
        impression.calculate_user_and_sdk()

        user = RedisDb(username)
        sdk = RedisDb(sdk_version)

    assert user.get_dict() == resource_data_after_increment
    assert sdk.get_dict() == resource_data_after_increment
