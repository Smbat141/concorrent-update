from flask_restful import Resource
from inbound_request.inbound_request import InboundRequest
from .statistics_calculator import StatisticsCalculator
import json


class Statistics(Resource, InboundRequest):
    filter_permitted_params = ['username', 'sdk']

    def get(self):
        if self.filter_params['is_valid']:
            general_statistics = StatisticsCalculator(self.filter_params["filter_by"], None)
            statistics_response = general_statistics.calculate_stats()

            return statistics_response
        else:
            return {'success': False, 'message': self.filter_params['message']}, 400
