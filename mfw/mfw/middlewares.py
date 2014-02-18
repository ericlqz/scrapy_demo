import random

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        fd = open('/home/eric/workspace/python/record.txt', 'r')
        data = fd.readlines()
        fd.close()
        length = len(data)
        index = random.randint(0, length-1)
        item = data[index]
        arr = item.strip('\n').split('\t')
        request.meta['proxy'] = 'http://%s:%s' % (arr[0], arr[1])
        # request.meta['proxy'] = 'http://%s:%s' % ('219.136.135.2', '9999')
        print 'use "%s" as request proxy for url: %s' % (request.meta['proxy'], request.url)
