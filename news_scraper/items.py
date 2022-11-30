import scrapy


class LinkItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    publishedAt = scrapy.Field()
    image = scrapy.Field()
