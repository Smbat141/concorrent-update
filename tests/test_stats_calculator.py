from redis_db.redis import RedisDb
from statistics.statistics_calculator import StatisticsCalculator


def test_statistics_calculator_calculate_ad(app):
    resource_data_before_increment = {'ad_requests_count': 0}
    resource_data_after_increment = {'ad_requests_count': 2}

    with app.test_request_context():
        resource_key = 'resource_name_1'
        stats_calc = StatisticsCalculator(resource_key, resource_data_before_increment)

        stats_calc.calculate_ad()
        stats_calc.calculate_ad()

        resource_data = RedisDb(resource_key).get_dict()

    assert resource_data == resource_data_after_increment


def test_statistics_calculator_calculate_impressions(app):
    resource_data_before_increment = {'impressions_requests_count': 0}
    resource_data_after_increment = {'impressions_requests_count': 2}

    with app.test_request_context():
        resource_key = 'resource_name_1'
        stats_calc = StatisticsCalculator(resource_key, resource_data_before_increment)

        stats_calc.calculate_impression()
        stats_calc.calculate_impression()

        resource_data = RedisDb(resource_key).get_dict()

    assert resource_data == resource_data_after_increment


def test_statistics_calculator_calculate_general_stats(app):
    resource_data = {'ad_requests_count': 0, 'impressions_requests_count': 0}

    resource_key = 'resource_name_1'
    stats_calc = StatisticsCalculator(resource_key, resource_data)

    general_stats = ({'success': True, resource_key: {
        'impressions': 10,
        'ad_requests': 10,
        'fill_rate': 1.0
    }}, 200)

    with app.test_request_context():
        # prepare some data for comparison
        for _ in range(10):
            stats_calc.calculate_ad()
            stats_calc.calculate_impression()

        resource_data = stats_calc.calculate_stats()

    assert resource_data == general_stats
