# Scrapy settings for rosi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'rosi'

SPIDER_MODULES = ['rosi.spiders']
NEWSPIDER_MODULE = 'rosi.spiders'

# For Image Downloade
ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
IMAGES_STORE = '/home/eric/workspace/python/rosi/rosi/images'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'rosi (+http://www.yourdomain.com)'

LOG_ENABLE = True
LOG_ENCODING = 'utf-8'
LOG_FILE = '/home/eric/workspace/python/rosi/rosi/log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = False
