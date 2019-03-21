import os

DEFAULT_TIMEOUT = 10000  # 10s
# TODO: add environ or try for int()
MAX_HTTP_CONNECTIONS = int(os.getenv('MAX_HTTP_CONNECTIONS'))
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
MSG_LIMIT = 10
SEARCH_URL = 'https://www.bing.com/search?q={q}&format=rss&count={limit}'
