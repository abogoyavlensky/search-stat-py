from itertools import groupby
from urllib.parse import urlparse

import requests

import feedparser
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse

MSG_LIMIT = 10
SEARCH_URL = 'https://www.bing.com/search?q={q}&format=rss&count={limit}'

app = Starlette(debug=True)


def get_domain(link):
    """Return second level domain from passed link."""
    parsed_url = urlparse(link)
    domains = parsed_url.netloc.split('.')[-2:]
    return '.'.join(domains)


def count_domains(links):
    """Return link dict grouped by domain."""
    groups = {}
    data = sorted(links, key=get_domain)
    for key, group in groupby(data, get_domain):
        groups[key] = list(group)
    return groups


def perform_request(query):
    """Perform search request to eternal service and return lisk of domains."""
    url = SEARCH_URL.format(q=query, limit=MSG_LIMIT)
    # TODO: uncomment
    # response = requests.get(url)
    # response.raise_for_status()
    # feed = feedparser.parse(url)
    # links = [entry['link'] for entry in feed.entries]
    # TODO: remove
    links = ['https://en.wikipedia.org/wiki/Lisp', 'https://de.wikipedia.org/wiki/Lisp', 'http://paulgraham.com/rootsoflisp.html', 'http://www.tutorialspoint.com/lisp/', 'http://e-words.jp/w/LISP.html',
             'http://www.lispworks.com/documentation/HyperSpec/Front/index.htm', 'http://www.lispworks.com/', 'http://sbcl.org/', 'https://www.dictionary.com/browse/lisp', 'http://www.lisp.sr/']
    # return list(map(get_domain, links))
    return count_domains(links)


@app.route('/search')
def search(request):
    query = request.query_params.getlist('query')

    # g = group([
    # frobnicate.message(1, 2),
    # frobnicate.message(2, 3),
    # frobnicate.message(3, 4),
    # ]).run()

    stat = perform_request(query[0])
    print(stat)

    return JSONResponse({'hello': query})
