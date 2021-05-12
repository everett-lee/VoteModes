import json
import boto3
import os

AWS_PROFILE = os.getenv('AWS_PROFILE')
TABLE_NAME = 'MPs'
dynamodb = None

if (AWS_PROFILE == 'localstack'):
    dynamodb = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                            endpoint_url='http://localhost:4566')
else:
    print("AWS profile: {profile} is not valid".format(profile=AWS_PROFILE))

def put_data():
    with open('../downloader/raw/rawMPList', 'r') as rawMps:
        mps = json.load(rawMps)['Data']

        for mp in mps:

            mp_id = mp['MemberId']
            name = mp['Name']

            table.put_item(
                Item={
                    'MemberId': mp_id,
                    'Name': name,
                }
            )

if dynamodb:
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'MemberId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'Name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'MemberId',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'Name',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        put_data()

    except Exception as err:
        print(err)