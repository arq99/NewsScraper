import os

from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

import yake


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
