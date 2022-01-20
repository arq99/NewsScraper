import os

from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv


class FirestorePipeline:
    def __init__(self):
        load_dotenv(find_dotenv())
        client = MongoClient(f"mongodb+srv://"
                             f"{os.environ.get('MDB_USERNAME')}:"
                             f"{os.environ.get('MDB_PASSWORD')}"
                             f"@news-search.kpgz8.mongodb.net/News-Search?retryWrites=true&w=majority")
        self.db = client.newsarticles

    def process_item(self, item, spider):
        news_article = {
            'source': item['source'],
            'url': item['url'],
            'title': item['title'],
            'date': item['date'],
            'article': item['article'],
        }

        #self.db.articles.insert_one(news_article)

        return item


