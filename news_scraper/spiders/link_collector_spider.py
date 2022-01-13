import scrapy

from urllib.parse import urlparse
from news_scraper.specifications import specs


class LinkCollector(scrapy.Spider):
    name = "link-collector"

    def start_requests(self):
        urls = []

        for links in specs.specs:
            urls = specs.specs[links]['links'] + urls

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        domain = urlparse(response.request.url).netloc

        section_css = specs.specs[domain]['section']
        url_css = specs.specs[domain]['url']

        for article in response.css(section_css):
            url = article.css(url_css).get()
            if url:
                yield {
                    'link': f'{domain}{url}'
                }
