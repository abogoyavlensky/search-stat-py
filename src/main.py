import itertools
import json
import logging
import typing
from collections import Counter
from typing import Dict, List
from urllib.parse import urlparse

import dramatiq
import feedparser
import requests
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from config import DEFAULT_TIMEOUT
from tasks import get_links

app = Starlette(debug=True)


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(",", ":"),
        ).encode("utf-8")


def get_domain(link: str) -> str:
    """Return second level domain from passed link."""
    parsed_url = urlparse(link)
    domains = parsed_url.netloc.split('.')[-2:]
    return '.'.join(domains)


def count_domains(links: List[str]) -> Dict[str, int]:
    """Return dict with counted domains."""
    domains = map(get_domain, set(links))
    return Counter(sorted(domains))


@app.route('/search')
def search(request: requests.Request) -> requests.Response:
    """Return statistic by domains which were found by passed query."""
    query = set(request.query_params.getlist('query'))
    logging.info('Searching statistic for [%(q)s]...', {'q': ', '.join(query)})
    group = dramatiq.group([get_links.message(word) for word in query]).run()
    results = group.get_results(block=True, timeout=DEFAULT_TIMEOUT)
    links = list(itertools.chain.from_iterable(results))
    data = count_domains(links)
    return PrettyJSONResponse(data)
