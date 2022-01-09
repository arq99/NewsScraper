import scrapy


class QuotesSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = [
            'https://www.nytimes.com/section/world',
            'https://www.nytimes.com/section/business',
            'https://www.nytimes.com/section/tech',
            'https://www.nytimes.com/section/science',
            'https://www.nytimes.com/section/sports',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article in response.css('li.css-ye6x8s'):
            title = article.css('h2.css-1j9dxys::text').get()
            summary = article.css('p.css-1echdzn::text').get()
            authors = article.css('span.css-1n7hynb::text').get()
            link = article.css('a::attr(href)').get()

            if title and summary and authors and link:
                yield {
                    'title': title,
                    'summary': summary,
                    'authors': authors,
                    'link': f'https://www.nytimes.com{link}'
                }
