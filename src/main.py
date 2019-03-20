import itertools
from collections import Counter
from urllib.parse import urlparse

import dramatiq
import feedparser
import requests
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from tasks import get_links

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


@app.route('/search')
def search(request):
    """Return statistic by domains which were found by passed query."""
    query = set(request.query_params.getlist('query'))
    group = dramatiq.group([get_links.message(word) for word in query]).run()
    results = group.get_results(block=True, timeout=DEFAULT_TIMEOUT)
    links = list(itertools.chain.from_iterable(results))
    data = count_domains(links)
    return JSONResponse(data)
