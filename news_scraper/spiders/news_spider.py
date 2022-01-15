import os

import scrapy
from newsapi import NewsApiClient
from dotenv import load_dotenv, find_dotenv

from ..items import LinkItem


class NewsSpider(scrapy.Spider):
    name = "links"

    def start_requests(self):
        load_dotenv(find_dotenv())
        newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

        all_articles = newsapi.get_everything(
            sources='abc-news',
            domains='abc-news.go.com',
            from_param='2022-01-01',
            to='2022-01-02',
            language='en',
            page_size=100
        )

        for data in all_articles['articles']:
            source = data['source']['name']
            url = data['url']
            title = data['title']
            url_to_image = data['urlToImage']
            published_at = data['publishedAt']

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    'source': source,
                    'url': url,
                    'title': title,
                    'urltoimage': url_to_image,
                    'publishedat': published_at,
                }
            )

    def parse(self, response):
        link = LinkItem()

        link['source'] = response.meta['source']
        link['url'] = response.meta['url']
        link['title'] = response.meta['title']
        link['urltoimage'] = response.meta['urltoimage']
        link['date'] = response.meta['publishedat']
        link['article'] = response.css('section.Article__Content p::text').getall()

        print(link)

        yield link
