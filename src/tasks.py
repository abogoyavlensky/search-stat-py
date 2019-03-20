import logging
from os.path import commonpath

import dramatiq
import feedparser
import requests
from dramatiq.brokers.redis import RedisBroker
from dramatiq.rate_limits import ConcurrentRateLimiter
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

REDIS_HOST = 'redis'
REDIS_PORT = 6379
MSG_LIMIT = 10
SEARCH_URL = 'https://www.bing.com/search?q={q}&format=rss&count={limit}'
MAX_HTTP_CONNECTIONS = 1

result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT)
broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

HTTP_CONNECTION_LIMITER = ConcurrentRateLimiter(
  result_backend, 'http-connection-limiter', limit=MAX_HTTP_CONNECTIONS)


@dramatiq.actor(store_results=True)
def get_links(query):
    # TODO: uncomment
    # with HTTP_CONNECTION_LIMITER.acquire(raise_on_failure=False) as acquired:
    url = SEARCH_URL.format(q=query, limit=MSG_LIMIT)
    response = requests.get(url)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    links = [entry['link'] for entry in feed.entries]
    logging.info(
        'Status: {} | Query: {} | Found links: {}'.format(
            response.status_code, query, links
        )
    )
    return links
