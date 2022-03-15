import requests
from flask import Response
from flask_restful import Resource
from statistics.statistics_calculator import StatisticsCalculator
from inbound_request.inbound_request import InboundRequest


class Ad(Resource, InboundRequest):
    permitted_params = ['sdk_version', 'session_id', 'platform', 'username', 'country_code']
    external_vast_xml_endpoint = 'https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast'

    def get(self):
        if self.params['is_valid']:
            self.calculate_user_and_sdk()
            return self.get_vast_xml()

        return {'success': False, 'message': self.params['message']}, 400

    def get_vast_xml(self):
        response = requests.get(self.external_vast_xml_endpoint)
        if response.status_code == 200:
            return Response(response.content, mimetype='application/xml')

        return {'message': 'Sorry, bad request'}, response.status_code

    def calculate_user_and_sdk(self):
        StatisticsCalculator(self.params['params']['username'], {"ad_requests_count": 0}).calculate_ad()
        StatisticsCalculator(self.params['params']['sdk_version'], {"ad_requests_count": 0}).calculate_ad()
