# -*- coding: utf-8 -*-
from scrapy.item import Item, Field

class MfwItem(Item):
    uid = Field()
    tid = Field()
    author = Field()
    title = Field()
    url = Field()
    content = Field()

    def __str__(self):
        return 'MfwItem(url: %s || title: %s)' % (self['url'], self['title'])

    def __unicode__(self):
        return 'MfwItem(url: %s || title: %s)' % (self['url'], self['title'])
