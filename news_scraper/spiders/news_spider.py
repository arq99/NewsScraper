import os
from datetime import datetime

import scrapy
from newsapi import NewsApiClient
from dotenv import load_dotenv, find_dotenv

from ..items import LinkItem


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        load_dotenv(find_dotenv())
        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        all_articles = newsapi.get_everything(
            sources='abc-news',
            domains='abc-news.go.com',
            from_param=datetime.today().strftime('%Y-%m-%d'),
            language='en',
            page_size=100
        )

        for data in all_articles['articles']:
            source = data['source']['name']
            url = data['url']
            title = data['title']
            published_at = data['publishedAt']

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    'source': source,
                    'url': url,
                    'title': title,
                    'publishedAt': published_at,
                }
            )

    def parse(self, response):
        link = LinkItem()

        link['source'] = response.meta['source']
        link['url'] = response.meta['url']
        link['title'] = response.meta['title']
        link['date'] = response.meta['publishedAt']
        link['summary'] = response.css('p.Article__Headline__Desc::text').getall()

        yield link
