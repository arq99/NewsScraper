import boto3


class DynamoDBPipeline:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('news-articles')

    def process_item(self, item, spider):
        self.table.put_item(
            Item={
                'source': item['source'],
                'url': item['url'],
                'title': item['title'],
                'date': item['date'],
                'article': item['article'],
            }
        )

        return item

