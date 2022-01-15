# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from google.cloud import firestore


class LinksPipeline:

    def __init__(self):
        db = firestore.Client(project='my-project-id')

    def process_item(self, item, spider):
        print("__________________________________________")
        return item
