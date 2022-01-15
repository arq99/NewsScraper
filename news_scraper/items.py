# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    urltoimage = scrapy.Field()
    date = scrapy.Field()
    article = scrapy.Field()
