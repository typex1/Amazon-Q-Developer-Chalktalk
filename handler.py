import json
import os
import boto3
import requests

# read password from environment variable
# password = os.environ['PASSWORD']

# create http headers
headers = {
    'Content-Type': 'application/json'
}
url = 'https://api.example.com'
# make http request with password
response = requests.get(url, auth=('user', password))

# read table name from environment variable
TABLE_NAME = os.environ['TABLE_NAME']
# create dynamodb resource
dynamodb = boto3.resource('dynamodb')
# create table object
table = dynamodb.Table(TABLE_NAME)

# add a function that creates a dynamodb table
def create_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

# perform sentiment analysis
def sentiment_analysis(text):
    comprehend = boto3.client(service_name='comprehend')
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return sentiment['Sentiment']

# log aws security credentials
print(os.environ['AWS_ACCESS_KEY_ID'])


def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    # extract the body from the evnent json data
    body = json.loads(event['body'])
    # extract the text from the body
    text = body['text']
    # perform sentiment analysis on the text
    sentiment = sentiment_analysis(text)
    # create new table item in the dynamodb table
    table.put_item(
        Item={
            'id': text,
            'sentiment': sentiment
        }
    )

    # return sentiment
    return {
        'statusCode': 200,
        'body': json.dumps({
            'sentiment': sentiment
        }
        )
    }