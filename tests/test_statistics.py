import json
from statistics.statistics_calculator import StatisticsCalculator
from statistics.statistics import Statistics


def binary_to_json(binary):
    return json.loads(binary.decode('utf8'))


def test_statistics_get_without_filter(client):
    failed_response = {'success': False,
                       'message': "following params are required ['username', 'sdk']"}

    response = binary_to_json(client.get('/statistics').data)

    assert response == failed_response


def test_statistics_get_success(client, mocker):
    successful_response = {'user_1': {
        'impressions': 2,
        'ad_requests': 5,
        'fill_rate': 0.4
    }}

    filter = {'username': 'user_1'}
    mocker.patch.object(StatisticsCalculator, 'calculate_stats', return_value=successful_response)
    response = binary_to_json(client.get('/statistics', query_string=filter).data)

    assert response == successful_response
