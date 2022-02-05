import scrapy


class LinkItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    image = scrapy.Field()
    article = scrapy.Field()
