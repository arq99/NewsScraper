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
        newsarticle = {
            'source': item['source'],
            'url': item['url'],
            'title': item['title'],
            'date': item['date'],
            'summary': item['summary'],
        }

        self.db.articles.insert_one(newsarticle)

        return item


