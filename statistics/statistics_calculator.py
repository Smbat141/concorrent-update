from redis_db.redis import RedisDb


class StatisticsCalculator:

    def __init__(self, resource_key, initial_data):
        self.resource_key = resource_key
        self.db = RedisDb(self.resource_key)
        self.set_initial_data(initial_data)

    def calculate_ad(self):
        self.db.increment_dict_value(self.resource_key, "ad_requests_count", 1)

    def calculate_impression(self):
        self.db.increment_dict_value(self.resource_key, "impressions_requests_count", 1)

    def calculate_stats(self) -> tuple:
        resource = self.db.get_dict()

        if not resource:
            return {'success': False, 'message': f'{self.resource_key} not found'}, 404

        impressions = resource['impressions_requests_count']
        ad_requests = resource['ad_requests_count']
        fill_rate = 0

        if ad_requests:
            fill_rate = impressions / ad_requests

        return {'success': True, self.resource_key: {'impressions': impressions, 'ad_requests': ad_requests,
                                                     'fill_rate': fill_rate}}, 200

    def set_initial_data(self, data):
        if data:
            self.db.create_dict_if_not_exist(data)
