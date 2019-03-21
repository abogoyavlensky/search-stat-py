import logging
from typing import List

import dramatiq
import feedparser
import requests
from dramatiq.brokers.redis import RedisBroker
from dramatiq.rate_limits import ConcurrentRateLimiter
from dramatiq.rate_limits.backends import RedisBackend as RateLimiterBackend
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend

from config import (DEFAULT_TIMEOUT, MAX_HTTP_CONNECTIONS, MSG_LIMIT,
                    REDIS_HOST, REDIS_PORT, SEARCH_URL)

result_backend = RedisBackend(host=REDIS_HOST, port=REDIS_PORT)
limiter_backend = RateLimiterBackend(host=REDIS_HOST, port=REDIS_PORT)
broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

# Restriction to be sure that we are not exceeding the limit of connections
HTTP_CONNECTION_LIMITER = ConcurrentRateLimiter(
    limiter_backend, 'http-connection-limiter', limit=MAX_HTTP_CONNECTIONS)


@dramatiq.actor(store_results=True, max_backoff=100, max_retries=None,
                max_age=DEFAULT_TIMEOUT, queue_name='search-queue')
def get_links(query: str) -> List[str]:
    with HTTP_CONNECTION_LIMITER.acquire():
        url = SEARCH_URL.format(q=query, limit=MSG_LIMIT)
        response = requests.get(url)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        links = [entry['link'] for entry in feed.entries]
        logging.info(
            'Status: %(code)s | Query: %(q)s | Found links: %(links)s',
            {'code': response.status_code, 'q': query, 'links': links}
        )
        return links
