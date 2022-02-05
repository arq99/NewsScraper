import os


from pymongo import MongoClient
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

        news_article = {
            'source': item['source'],
            'url': item['url'],
            'title': item['title'],
            'date': item['date'],
            'image': item['image'],
            'article': item['article'],
        }

        if self.find_duplicate(item) is None:
            self.db.articles.insert_one(news_article)

        return item
