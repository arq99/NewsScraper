import random
from datetime import datetime

from google.cloud import firestore
from google.oauth2 import service_account


class LinksPipeline:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file("newssearch-cred.json")
        self.db = firestore.Client(project='newssearch-338106', credentials=credentials)

    def process_item(self, item, spider):
        #doc_ref = self.db.collection(u'news-article-links')\
        #    .document(f'{datetime.today().strftime("%Y-%m-%d")}')

        #a = doc_ref.collection(f'{random.randint(100000, 999999)}')\
        #    .document(f'link')

        #a.set({
        #    u'link': item['link'],
        #    u'date': item['date']
        #})
        return item
