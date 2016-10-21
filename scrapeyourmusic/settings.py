# Scrapy settings for scrapeyourmusic project

SPIDER_MODULES = ['scrapeyourmusic.spiders']
NEWSPIDER_MODULE = 'scrapeyourmusic.spiders'
DEFAULT_ITEM_CLASS = 'scrapeyourmusic.items.Album'

ITEM_PIPELINES = {'scrapeyourmusic.pipelines.FormatDataPipeline': 1}

FEED_URI = 'out/out.json'
FEED_FORMAT = 'json'

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 5.0
RANDOMIZE_DOWNLOAD_DELAY = True

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# ROBOTSTXT_OBEY = True

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'

RETRY_HTTP_CODES = [502, 500, 504, 408]

HTTPERROR_ALLOWED_CODES = [503]
