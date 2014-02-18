# Scrapy settings for mfw project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'mfw'

SPIDER_MODULES = ['mfw.spiders']
NEWSPIDER_MODULE = 'mfw.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mfw (+http://www.yourdomain.com)'
# DOWNLOAD_DELAY = 1
# RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOADER_MIDDLEWARES = {
    'mfw.middlewares.ProxyMiddleware': 751,
}

ITEM_PIPELINES = [
    'mfw.pipelines.MfwPipeline',
]

LOG_ENABLE = True
LOG_ENCODING = 'utf-8'
LOG_FILE = '/home/eric/workspace/python/mfw/log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = False
