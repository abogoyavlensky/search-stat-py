import logging
from typing import List

import dramatiq
import feedparser
import requests
from dramatiq.brokers.redis import RedisBroker
from dramatiq.brokers.stub import StubBroker
from dramatiq.rate_limits import ConcurrentRateLimiter
from dramatiq.rate_limits.backends import RedisBackend as RateLimiterBackend
from dramatiq.rate_limits.backends.stub import StubBackend as RateLimiterStub
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from dramatiq.results.backends.stub import StubBackend

from src import config

if not config.TESTING:
    result_backend = RedisBackend(
        host=config.REDIS_HOST, port=config.REDIS_PORT
    )
    limiter_backend = RateLimiterBackend(
        host=config.REDIS_HOST, port=config.REDIS_PORT
    )
    broker = RedisBroker(host=config.REDIS_HOST, port=config.REDIS_PORT)
else:
    result_backend = StubBackend()
    limiter_backend = RateLimiterStub()
    broker = StubBroker()
    broker.emit_after("process_boot")

broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)


# Restriction to be sure that we are not exceeding the limit of connections
HTTP_CONNECTION_LIMITER = ConcurrentRateLimiter(
    limiter_backend,
    "http-connection-limiter",
    limit=config.MAX_HTTP_CONNECTIONS,
)


@dramatiq.actor(
    store_results=True,
    max_backoff=100,
    max_retries=10,
    max_age=config.DEFAULT_TIMEOUT,
    queue_name="search-queue",
)
def get_links(query: str) -> List[str]:
    with HTTP_CONNECTION_LIMITER.acquire():
        url = config.SEARCH_URL.format(q=query, limit=config.MSG_LIMIT)
        response = requests.get(url)
        response.raise_for_status()  # will be retried upon exception
        feed = feedparser.parse(response.content)
        links = [entry["link"] for entry in feed.entries]
        logging.info(
            "Status: %(code)s | Query: %(q)s | Found links: %(links)s",
            {"code": response.status_code, "q": query, "links": links},
        )
        return links
