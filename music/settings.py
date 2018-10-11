# -*- coding: utf-8 -*-
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 64
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
# RETRY_HTTP_CODES = [503]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
LOG_LEVEL = 'INFO'
RETRY_TIMES = 5
ITEM_PIPELINES = {
    'pipelines.MusicPipeline': 800
}
