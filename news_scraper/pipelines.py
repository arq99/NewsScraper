import random
from datetime import datetime

from google.cloud import firestore
from google.oauth2 import service_account


class FirestorePipeline:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file("newssearch-cred.json")
        self.db = firestore.Client(project='newssearch-338106', credentials=credentials)

    def process_item(self, item, spider):
        doc_ref = self.db.collection(u'news-articles')\
            .document(f'{datetime.today().strftime("%Y-%m-%d")}')

        a = doc_ref.collection(f'{random.randint(100000, 999999)}')\
            .document(f'article-data')

        a.set({
            u'source': item['source'],
            u'url': item['url'],
            u'title': item['title'],
            u'date': item['date'],
            u'article': item['article'],
        })
        return item
