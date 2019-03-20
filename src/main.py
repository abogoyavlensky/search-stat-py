import itertools
from collections import Counter
from urllib.parse import urlparse

import feedparser
import requests
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from tasks import get_links, dramatiq

# MSG_LIMIT = 10
# SEARCH_URL = 'https://www.bing.com/search?q={q}&format=rss&count={limit}'
DEFAULT_TIMEOUT = 5000  # 5s

app = Starlette(debug=True)


def get_domain(link):
    """Return second level domain from passed link."""
    parsed_url = urlparse(link)
    domains = parsed_url.netloc.split('.')[-2:]
    return '.'.join(domains)


def count_domains(links):
    """Return dict with counted domains."""
    domains = map(get_domain, set(links))
    return Counter(sorted(domains))


# def perform_request(query):
#     """Perform search request to eternal service and return lisk of domains."""
#     url = SEARCH_URL.format(q=query, limit=MSG_LIMIT)
#     response = requests.get(url)
#     response.raise_for_status()
#     feed = feedparser.parse(url)
#     links = [entry['link'] for entry in feed.entries]
#     # TODO: remove
#     links = ['https://en.wikipedia.org/wiki/Lisp', 'https://de.wikipedia.org/wiki/Lisp', 'http://paulgraham.com/rootsoflisp.html', 'http://www.tutorialspoint.com/lisp/', 'http://e-words.jp/w/LISP.html',
#              'http://www.lispworks.com/documentation/HyperSpec/Front/index.htm', 'http://www.lispworks.com/', 'http://sbcl.org/', 'https://www.dictionary.com/browse/lisp', 'http://www.lisp.sr/']
#     return links


@app.route('/search')
def search(request):
    """Return statistic by domains which were found by passed query."""
    query = set(request.query_params.getlist('query'))

    group = dramatiq.group([get_links.message(word) for word in query]).run()
    # group.wait(timeout=DEFAULT_TIMEOUT)

    results = group.get_results(block=True, timeout=DEFAULT_TIMEOUT)
    for res in results:
        print(res)
    # print(results)
    # links = list(itertools.chain.from_iterable(results))
    # print(links)

    # # links = perform_request(query[0])
    # data = count_domains(links)
    # print(data)

    # get_links.send(query[0])
    # get_links.send(query[1])
    # [get_links.send(word) for word in query]

    # get_links(query[0])
    # get_links(query[1])


    return JSONResponse({})
