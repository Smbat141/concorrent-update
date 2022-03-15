import threading

import requests


def ad():
    for _ in range(10000):
        requests.get(
            'http://127.0.0.1:5000/ad?sdk_version=1.0&session_id=sdflskdhafksdfha&platform=Linux&username=Jack&country_code=CA')


def impression():
    for _ in range(10000):
        requests.get(
            'http://127.0.0.1:5000/impression?sdk_version=1.0&session_id=sdflskdhafksdfha&platform=Linux&username=Jack&country_code=CA')


threading.Thread(target=ad).start()
threading.Thread(target=impression).start()
