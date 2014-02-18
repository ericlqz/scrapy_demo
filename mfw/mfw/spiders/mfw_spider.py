# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from mfw.items import MfwItem

class MfwSpider(BaseSpider):
    name = "mfw"
    allowed_domains = ["mafengwo.cn"]
    prefix_url = "http://www.mafengwo.cn"
    start_urls = [
    ]
    for index in range(1, 246):
        url = "http://www.mafengwo.cn/yj/10035/1-0-%s.html" % index
        start_urls.append(url)

    def parse(self, response):
        items = []
        hxs = HtmlXPathSelector(response)
        articles = hxs.select('//h2[@class="post-title yahei"]/a/@href').extract()
        items.extend([self.make_requests_from_url(self.prefix_url+url).replace(callback=self.parse_post) for url in articles])
        for url in articles:
            print 'retrieve post url: %s' % self.prefix_url+url
        return items

    def parse_post(self, response):
        print 'parse_post url: %s' % response.url
        hxs = HtmlXPathSelector(response)
        post = hxs.select('//div[@class="post_main"]')
        item = MfwItem()
         
        # get user id
        uid = post.select("div[@class='post_item'][1]/div[@class='author_info']/div[@class='avatar_box']/div[@class='out_pic']/@val").extract()[0]
        item['uid'] = uid

        # set author 
        author_city = post.select("div[@class='post_item'][1]/div[@class='post_info']/div[@class='tools']/div[@class='fl']/a[@class='name']/text()").extract()[0]
        index = author_city.find('(')
        if index > 0:
            item['author'] = author_city[0:index]
        else:
            item['author'] = author_city

        # set tid 
        suffix = response.url.split("/")[-1]
        item['tid'] = suffix[0:suffix.find('.')]

        item = self.parse_item(response, item)
        yield item

        owner_str = '&ownerid=' + uid
        next = self.get_next_link(response, owner_str)
        if None != next:
            yield next
   
    # 对于下一页的解析
    def parse_next(self, response):
        print 'parse_next: %s' % response.url
        hxs = HtmlXPathSelector(response)
        post = hxs.select('//div[@class="post_main"]')
        item = MfwItem()

        owner_str = '&' + response.url.split('&')[-1] 
        uid = owner_str.split('=')[-1]
        item['uid'] = uid

        # set tid 
        suffix = response.url.split("=")[1]
        item['tid'] = suffix.split("&")[0]

        item = self.parse_item(response, item)
        yield item

        next = self.get_next_link(response, owner_str)
        if None != next:
            yield next

    def parse_item(self, response, item):
        hxs = HtmlXPathSelector(response)
        post = hxs.select('//div[@class="post_main"]')
        
        # set url
        item['url'] = unicode(response.url)

        # set title
        item['title'] = post.select("div[@class='post_title']/h1/text()").extract()[0]

        # set content
        uid = item['uid']
        con_group = post.select("div[@class='post_item']/div[@class='post_info']/div[@ownerid='"+uid+"']").extract()
        content = " =||= ".join(con_group)
        item['content'] = self.strip_tags(content)

        return item

    def get_next_link(self, response, owner_str):
        print 'get_next_link: %s' % response.url
        hxs = HtmlXPathSelector(response)
        post = hxs.select('//div[@class="post_main"]')
        # Next page
        page_links = post.select("div[@class='turn_page']/div[@class='paginator']/a")
        if len(page_links) > 0:
            link = page_links[-1]
            if link.select('text()').extract()[0] == u'\xa0Next\xa0>>':
                url = link.select('@href').extract()[0]
                return self.make_requests_from_url(self.prefix_url+url+owner_str).replace(callback=self.parse_next)
            else:
                print 'page_link[-1]: %s' % link.select('text()').extract()[0]
                return None
    
    def strip_tags(self, html):
        from HTMLParser import HTMLParser
        html=html.strip()
        html=html.strip("\n")
        html=html.replace('\r\n', '')
        result=[]
        parse=HTMLParser()
        parse.handle_data=result.append
        parse.feed(html)
        parse.close()
        return " ".join(result)
