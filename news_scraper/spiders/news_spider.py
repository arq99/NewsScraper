import os
from datetime import datetime
import requests

import scrapy
from dotenv import load_dotenv, find_dotenv

from ..items import LinkItem
from ..specifications import specs


class NewsSpider(scrapy.Spider):
    name = "news"
    
    
    def start_requests(self):
        load_dotenv(find_dotenv())

        url = f'https://newsdata.io/api/1/news?apikey={os.getenv("NEWS_API_KEY")}&domain=coindesk,cointelegraph'
        response = requests.get(url).json()

        for article in response['results']:
            print(article['title'])
            yield scrapy.Request(
                url=article['link'],
                callback=self.parse,
                meta={
                    'title': article['title'],
                    'url': article['link'],
                    'keywords': article['keywords'],
                    'description': article['description'],
                    'content': article['content'],
                    'publishedAt': article['pubDate'],
                    'image': article['image_url'],
                }
            )

    def parse(self, response):
        link = LinkItem()

        link['title'] = response.meta['title']
        link['url'] = response.meta['url']
        link['keywords'] = response.meta['keywords']
        link['description'] = response.meta['description']
        link['content'] = response.meta['content']
        link['publishedAt'] = response.meta['publishedAt']
        link['image'] = response.meta['image']

        yield link
    