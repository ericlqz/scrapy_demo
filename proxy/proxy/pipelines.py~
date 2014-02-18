# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import re,urllib,time,exceptions,socket

import codecs

#使用UTF-8格式保存文件
#fp = codecs.open('record.txt', 'a', 'utf-8')

class ProxyPipeline(object):
    def process_item(self, item, spider):
        port = item['port']
        port_re = re.compile('\d{1,5}')
        ports = port_re.findall(port)
        if len(ports) == 0:
            raise DropItem("can not find port in %s" % item['port'])
        else:
            item['port'] = ports[0]

        detect_service_url = 'http://www.mafengwo.cn/i/1151043.html'
        # detect_service_url = 'http://www.baidu.com'
        proxy_ = str('http://%s:%s' % (str(item['address']), str(item['port'])))
        proxies = {'http':proxy_}
        timeout = 1
        socket.setdefaulttimeout(timeout)
        try:
            data = urllib.urlopen(detect_service_url, proxies=proxies).read()
        except exceptions.IOError:
            raise DropItem("curl download the proxy %s:%s is bad" % (item['address'], str(item['port'])))
        if '' == data.strip():
            raise DropItem("data is null the proxy %s:%s is bad" % (item['address'], str(item['port'])))

        fp = open('record.txt', 'a')
        p = str(item['address']) + '\t' + str(item['port']) + '\n'
        fp.write(p)
        fp.close()
        return item
