import dramatiq
from starlette.testclient import TestClient
from src import config, main


def test_get_domain_ok():
    assert main.get_domain('https://dev.test.com/some/path') == 'test.com'


def test_get_domain_empty_link_ok():
    assert main.get_domain('') == ''


def test_count_domains_by_unique_links_ok():
    links = [
        'https://en.wikipedia.org/wiki/Lisp',
        'https://de.wikipedia.org/wiki/test',
        'http://google.com/rootsoflisp.html'
    ]
    assert main.count_domains(links) == {'wikipedia.org': 2, 'google.com': 1}


def test_count_domains_by_same_links_ok():
    links = [
        'https://en.wikipedia.org/wiki/Lisp',
        'http://google.com/rootsoflisp.html'
        'http://google.com/rootsoflisp.html'
    ]
    assert main.count_domains(links) == {'wikipedia.org': 1, 'google.com': 1}


def test_search_ok(mocker):
    group_mock = mocker.Mock(dramatiq.group)
    group_mock.get_results = mocker.Mock(return_value=[
        ['https://en.wikipedia.org/wiki/Lisp',
         'http://google.com/rootsoflisp.html'],
        ['https://de.wikipedia.org/wiki/test']])
    mocker.patch('dramatiq.group.run', return_value=group_mock)
    client = TestClient(main.app)
    response = client.get('/search')
    assert response.status_code == 200
    assert dir(response)
    assert response.json() == {'wikipedia.org': 2, 'google.com': 1}
