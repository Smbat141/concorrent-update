from typing import Sequence

from flask import request


class InboundRequest:
    permitted_params = []
    filter_permitted_params = []

    def __init__(self):
        self.params = self.fetch_permitted_params(self.permitted_params)
        self.filter_params = self.fetch_filter_params(self.filter_permitted_params)

    def fetch_permitted_params(self, permitted_params: Sequence[str]) -> dict:
        fetched_params = {}

        if permitted_params:
            for param in permitted_params:
                fetched_params[param] = request.args.get(param)

            if not self.is_there_mismatch(fetched_params):
                not_existed_params = [key for key, value in fetched_params.items() if value is None]
                message = f'following params are required {not_existed_params}'
                return {'is_valid': False, 'message': message}
        else:
            for key, value in request.args.items():
                fetched_params[key] = value

        return {'is_valid': True, 'params': fetched_params}

    def fetch_filter_params(self, filter_params: Sequence[str]) -> dict:

        # set filter_by from request first encountered param
        if filter_params:
            for key, value in request.args.items():
                if key in filter_params:
                    return {'is_valid': True, 'filter_by': value}

        return {'is_valid': False, 'message': f'following params are required {filter_params}'}

    @staticmethod
    def is_there_mismatch(dict_params: dict) -> bool:
        if None in dict_params.values(): return False
        return True
