import os

from pymongo import MongoClient
import boto3

import pandas as pd

from dotenv import load_dotenv, find_dotenv

class MongoDBPipeline:

    def __init__(self):
        load_dotenv(find_dotenv())
        
        client = MongoClient(
            f"mongodb+srv://"
            f"{os.environ.get('MDB_USERNAME')}:"
            f"{os.environ.get('MDB_PASSWORD')}"
            f"@news-search.kpgz8.mongodb.net/News-Search?retryWrites=true&w=majority")
    
        self.db = client.newsarticles
    
    # Check if the item is already in the database
    def find_duplicate(self, item):
        return self.db.articles.find_one({'url': item['url']})

    def process_item(self, item, spider):

        # Skip if description is empty
        if item['description'] == '':
            return item

        news_article = {
            'title': item['title'],
            'url': item['url'],
            'keywords': item['keywords'],
            'description': item['description'],
            'content': item['content'],
            'publishedAt': item['publishedAt'],
            'image': item['image'],
        }


        if self.find_duplicate(item) is None and item['image'] != 'null':
            self.db.articles.insert_one(news_article)

        return item

class DynamoDBPipeline:

    def __init__(self):
        load_dotenv(find_dotenv())
        
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = dynamodb.Table('newssearch')

    def process_item(self, item, spider):

        # Skip if description is empty
        if item['description'] == '':
            return item

        news_article = {
            'title': item['title'],
            'url': item['url'],
            'keywords': item['keywords'],
            'description': item['description'],
            'content': item['content'],
            'date': item['publishedAt'],
            'image': item['image'],
            'category': 'latest',
        }

        # Check if the item is already in the database using the category and date and filter for url
        response = self.table.get_item(
            Key={
                'category': 'latest',
                'date': item['publishedAt']
            }
        )

        if 'Item' not in response:
            self.table.put_item(Item=news_article)

        return item