import os
import requests

import scrapy
from dotenv import load_dotenv, find_dotenv

from ..items import LinkItem


class NewsSpider(scrapy.Spider):
    name = "news"
    
    
    def start_requests(self):
        load_dotenv(find_dotenv())

        url = f'https://newsdata.io/api/1/news?apikey={os.getenv("NEWS_API_KEY")}&domain=cointelegraph,decrypt'
        response = requests.get(url).json()

        for article in response['results']:
            yield scrapy.Request(
                url=article['link'],
                callback=self.parse,
                meta={
                    'title': article['title'],
                    'url': article['link'],
                    'description': article['description'],
                    'content': '',
                    'publishedAt': article['pubDate'],
                    'image': article['image_url']
                }
            )
            break
            

    def parse(self, response):
        link = LinkItem()

        link['title'] = response.meta['title']
        link['url'] = response.meta['url']
        link['description'] = response.meta['description']
        link['content'] = response.meta['content']
        link['publishedAt'] = response.meta['publishedAt']
        link['image'] = response.meta['image']

        yield link
    
    # Run command after scraping is complete
    def close(spider, reason):
        pass

    