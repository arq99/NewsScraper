import os
from datetime import datetime

import scrapy
from newsapi import NewsApiClient
from dotenv import load_dotenv, find_dotenv

from ..items import LinkItem
from ..specifications import specs


class NewsSpider(scrapy.Spider):
    name = "news"
    
    
    def start_requests(self):
        load_dotenv(find_dotenv())
        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        for spec in specs.specs:
            data = newsapi.get_everything(
                sources=specs.specs[spec]['sources'],
                domains=specs.specs[spec]['domains'],
                from_param=datetime.today().strftime('%Y-%m-%d'),
                language='en',
                page_size=100
            )

            data = data['articles']

            for article in data:
                source = article['source']['name']
                url = article['url']
                title = article['title']
                published_at = article['publishedAt']
                image = article['urlToImage']

                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={
                        'source': source,
                        'url': url,
                        'title': title,
                        'publishedAt': published_at,
                        'image': image,
                        'article' : specs.specs[spec]['article']
                    }
                )

    def parse(self, response):
        link = LinkItem()

        link['source'] = response.meta['source']
        link['url'] = response.meta['url']
        link['title'] = response.meta['title']
        link['date'] = response.meta['publishedAt']
        link['image'] = response.meta['image']
        link['article'] = response.css(response.meta['article']).getall()

        yield link
    