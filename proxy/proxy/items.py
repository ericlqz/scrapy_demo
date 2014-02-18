from scrapy.item import Item, Field

class ProxyItem(Item):
    address   = Field()
    port      = Field()
    protocol  = Field()
    location  = Field()

    type      = Field() # 0: anonymity #1: nonanonymity
    delay     = Field() # in second
    timestamp = Field()
