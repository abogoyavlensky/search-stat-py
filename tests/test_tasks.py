import os

import requests
from src.tasks import get_links


def test_search_ok(mocker):
    response_mock = mocker.Mock(requests.Response)
    response_mock.raise_for_status = mocker.Mock(return_value=None)
    response_mock.status_code = 200
    with open(os.path.join(os.path.dirname(__file__), 'search.xml')) as f:
        response_mock.content = f.read()
    mocker.patch('requests.get', return_value=response_mock)
    assert get_links('test') == [
        'https://www.speedtest.net/',
        'https://test.tankionline.com/',
        'https://ru.wikipedia.org/wiki/Test'
    ]
