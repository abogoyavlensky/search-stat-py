from environs import Env

env = Env()

DEFAULT_TIMEOUT = 10000  # 10s
MAX_HTTP_CONNECTIONS = env.int('MAX_HTTP_CONNECTIONS')
REDIS_HOST = env('REDIS_HOST', 'redis')
REDIS_PORT = env.int('REDIS_PORT', 6379)
MSG_LIMIT = 10
SEARCH_URL = 'https://www.bing.com/search?q={q}&format=rss&count={limit}'
