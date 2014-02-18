# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from proxy.items import ProxyItem
import re

class ProxycrawlerSpider(CrawlSpider):
    name = 'cnproxy'
    allowed_domains = ['www.cnproxy.com']
    indexes = [1,2,3,4,5,6,7,8.9,10]
    start_urls = []
    for i in indexes:
        url = 'http://www.cnproxy.com/proxy%s.html' %i
        start_urls.append(url)
    start_urls.append('http://www.cnproxy.com/proxyedu1.html')
    start_urls.append('http://www.cnproxy.com/proxyedu2.html')

    def parse(self, response):
        items = []
        hxs = HtmlXPathSelector(response)
        addresses = hxs.select('//tr[position()>1]/td[position()=1]').re('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        protocols = hxs.select('//tr[position()>1]/td[position()=2]').re('<td>(.*)<\/td>')
        locations = hxs.select('//tr[position()>1]/td[position()=4]').re('<td>(.*)<\/td>')
        ports_re = re.compile('write\(":"(.*)\)</S')
        raw_ports = ports_re.findall(response.body);
        port_map = {
            'a':'2','b':'5',
            'c':'1','i':'7',
            'l':'9','m':'4',
            'q':'0','r':'8',
            'v':'3','w':'6',
            '+':''
        }
        ports = []
        for port in raw_ports:
            tmp = port
            for key in port_map:
                tmp = tmp.replace(key, port_map[key])
            ports.append(tmp)

        for i in range(len(addresses)):
            item = ProxyItem()
            item['address'] = addresses[i]
            item['protocol'] = protocols[i]
            item['location'] = locations[i]
            item['port'] = ports[i]
            items.append(item)
        return items
