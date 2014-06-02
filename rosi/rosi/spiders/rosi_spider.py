#!/usr/bin/env python
# encoding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from rosi.items import RosiItem
import re


class RosiSpider(CrawlSpider):
    """ Spider for Rosimn """

    name = 'Rosimn'
    allow_domains = ['rosimn.com']
    start_urls = ['http://www.rosimn.com/x/']
    rules = [
        Rule(SgmlLinkExtractor(allow=['/x/list-\d+.htm']), follow = True, process_links = 'filter_listpage'),
        Rule(SgmlLinkExtractor(allow=['/x/album-\d+.htm']), callback = "parse_item")
    ]

    listed_urls = ['http://www.rosimn.com/x/list-1.htm']

    def filter_listpage(self, links):
        filter_links = []
        for link in links:
            if link.url not in self.listed_urls:
                filter_links.append(link)
                self.listed_urls.append(link.url)
                self.log("Check link: " + link.url)

        return filter_links

    def parse_item(self, response):
        """ Parse the album. And Download the images """

        self.log("Parse album page: " + response.url)
        sel = Selector(response)
        album = RosiItem()
        album['url'] = response.url
        album['albumId'] =  re.findall(r'[\d]+', response.url)[0]
        album['image_urls']= sel.xpath('//div[contains(@class, "album-thumbs album-thumbs-free")]/a/@href').extract()

        return album
