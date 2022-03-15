from flask import Flask
from flask_restful import Api
from ad.ad import Ad
from impression.impression import Impression
from statistics.statistics import Statistics


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Ad, '/ad')
    api.add_resource(Impression, '/impression')
    api.add_resource(Statistics, '/statistics')
    return app
