#!/bin/bash
dramatiq-gevent tasks -t $MAX_HTTP_CONNECTIONS -p 1 --queues search-queue --watch .
