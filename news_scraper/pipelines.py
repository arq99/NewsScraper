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
            'source': item['source'],
            'url': item['url'],
            'title': item['title'],
            'date': item['date'],
            'image': item['image'],
            'keywords': item['keywords'],
        }

        if self.find_duplicate(item) is None and item['image'] is not None:
            self.db.articles.insert_one(news_article)

        return item

# Pipeline to extract keywords from the article using TfidfVectorizer
class KeywordExtractionPipeline:
    def __init__(self):
        kw_extractor = yake.KeywordExtractor()
        self.custom_kw_extractor = yake.KeywordExtractor(
            lan="en", 
            n=3, 
            dedupLim=0.9, 
            top=20, 
            features=None
        )

    def process_item(self, item, spider):
        text = ""
        for sentence in item['article']:
            text += sentence
        
        keywords = self.custom_kw_extractor.extract_keywords(text)

        item['keywords'] = keywords

        return item
