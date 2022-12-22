import os

from pymongo import MongoClient
import boto3

import re

from newspaper import Article

from dotenv import load_dotenv, find_dotenv

class ContentExtractorPipeline:

    def process_item(self, item, spider):

        url = item['url']
        article = Article(url, keep_article_html=True)
        article.download()
        article.parse()

        a = article.article_html
        # Set the content
        item['content'] = a

        return item


class DynamoDBPipeline:

    def __init__(self):
        load_dotenv(find_dotenv())
        
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = dynamodb.Table('newssearch')

    def process_item(self, item, spider):

        print('------------------------------------')
        print(item)
        
        # Get the date in format YYYY/MM/DD
        date = str(item['publishedAt'])
        date = date[:10]
        date = date.replace('-', '/')

        # Remove all special characters from the title using regex
        title = item['title'].replace(' ', '-')
        title = title.replace('?', '')
        title = title.replace('!', '')
        title = title.replace('(', '')
        title = title.replace(')', '')

        # Remove spaces from the title and replace with dashes
        title = item['title'].replace(' ', '-')

        # Using regex to remove all special characters from the title but keep spaces and dashes
        title2 = re.sub(r'[^\w\s-]', '', title)

        url = f'{date}/{title2}'

        print(url)

        news_article = {
            'title': item['title'],
            'url': url,
            'description': item['description'],
            'content': item['content'],
            'date': item['publishedAt'],
            'image': item['image'],
            'searchquery': 'latest',
        }

        # Check if the item is already in the database using the category and date and filter for url
        response = self.table.get_item(
            Key={
                'searchquery': 'latest',
                'date': item['publishedAt']
            }
        )

        if 'Item' not in response:
            self.table.put_item(Item=news_article)

        return item

class DynamoDBPipeline2:
    def __init__(self):
        load_dotenv(find_dotenv())
        
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = dynamodb.Table('articles')

    def process_item(self, item, spider):
        
        # Get the date in format YYYY/MM/DD
        date = str(item['publishedAt'])
        date = date[:10]
        date = date.replace('-', '/')

        # Remove spaces from the title and replace with dashes
        title = item['title'].replace(' ', '-')

        # Using regex to remove all special characters from the title but keep spaces and dashes
        title2 = re.sub(r'[^\w\s-]', '', title)

        url = f'{date}/{title2}'

        news_article = {
            'id': url,
            'title': item['title'],
            'description': item['description'],
            'content': item['content'],
            'date': item['publishedAt'],
            'image': item['image'],
        }

        # Check if the item is already in the database using the category and date and filter for url
        response = self.table.get_item(
            Key={
                'id': url
            }
        )

        if 'Item' not in response:
            self.table.put_item(Item=news_article)

        return item
