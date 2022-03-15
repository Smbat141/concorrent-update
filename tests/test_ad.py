import json
import requests
from ad.ad import Ad
from redis_db.redis import RedisDb
import xml.etree.ElementTree as ET


def binary_to_json(binary):
    return json.loads(binary.decode('utf8'))


def dict_without_keys(dct, keys):
    return {key: dct[key] for key in dct if key not in keys}


def test_ad_get_without_permitted_params(client):
    failed_response = {'success': False,
                       'message': "following params are required ['sdk_version', 'session_id', 'platform', 'username', 'country_code']"}

    response = binary_to_json(client.get('/ad').data)
    assert response == failed_response


def test_ad_get_without_sdk_version(client, query_params):
    failed_response = {'success': False, 'message': "following params are required ['sdk_version']"}
    query_params_without_sdk_version = dict_without_keys(query_params, ['sdk_version'])
    response = binary_to_json(client.get('/ad', query_string=query_params_without_sdk_version).data)
    assert response == failed_response


def test_ad_get_without_username(client, query_params):
    failed_response = {'success': False,
                       'message': "following params are required ['username']"}

    query_params_without_username = dict_without_keys(query_params, ['username'])
    response = binary_to_json(client.get('/ad', query_string=query_params_without_username).data)

    assert response == failed_response


def test_ad_get_method_success(client, query_params, mocker):
    successful_response = {'success': True}
    # mock function for calculate and get_xml and return simple message
    mocker.patch.object(Ad, 'get_vast_xml', return_value=successful_response)
    mocker.patch.object(Ad, 'calculate_user_and_sdk', return_value=successful_response)

    response = binary_to_json(client.get('/ad', query_string=query_params).data)

    assert response == successful_response


def test_ad_get_vast_xml_with_failed_response(app, mocker):
    failed_response = {'message': 'Sorry, bad request'}, 500

    with app.test_request_context():
        # stub for request get method
        request_object = mocker.stub()
        request_object.status_code = 500

        mocker.patch.object(requests, 'get', return_value=request_object)

        response = Ad().get_vast_xml()

    assert response == failed_response


def test_ad_get_vast_xml_success(app, mocker):
    response_xml = '<test><body>Vast Xml</body></test>'
    expected_xml = ET.ElementTree(ET.fromstring(response_xml))

    with app.test_request_context():
        # stub for request get method
        request_object = mocker.stub()
        request_object.status_code = 200
        request_object.content = expected_xml

        mocker.patch.object(requests, 'get', return_value=request_object)

        xml_from_method = Ad().get_vast_xml().response

    assert xml_from_method == expected_xml


def test_ad_calculate_user_and_sdk(app):
    resource_data_after_increment = {'ad_requests_count': 2}
    with app.test_request_context():
        ad = Ad()
        username = 'user_1'
        sdk_version = '1.0'
        ad.params = {'params': {'username': username, "sdk_version": sdk_version}}

        ad.calculate_user_and_sdk()
        ad.calculate_user_and_sdk()

        user = RedisDb(username)
        sdk = RedisDb(sdk_version)

    assert user.get_dict() == resource_data_after_increment
    assert sdk.get_dict() == resource_data_after_increment
