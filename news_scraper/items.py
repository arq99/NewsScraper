import scrapy


class LinkItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    urltoimage = scrapy.Field()
    date = scrapy.Field()
    article = scrapy.Field()
