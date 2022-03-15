from flask_restful import Resource
from inbound_request.inbound_request import InboundRequest
from statistics.statistics_calculator import StatisticsCalculator


class Impression(Resource, InboundRequest):
    permitted_params = ['sdk_version', 'session_id', 'platform', 'username', 'country_code']

    def get(self):
        if self.params['is_valid']:
            self.calculate_user_and_sdk()
            return {'success': True, 'message': 'Successfully fetched'}, 200
        return {'success': False, 'message': self.params['message']}, 400

    def calculate_user_and_sdk(self):
        StatisticsCalculator(self.params['params']['username'],
                             {"impressions_requests_count": 0}).calculate_impression()

        StatisticsCalculator(self.params['params']['sdk_version'],
                             {"impressions_requests_count": 0}).calculate_impression()
