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
            member_id = mp['MemberId']
            name = mp['Name']

            table.put_item(
                Item={
                    'MPElectionYear': 2019,
                    'MemberId': member_id,
                    'Name': name,
                    'Votes': []
                }
            )

if dynamodb:
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'MPElectionYear',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'MemberId',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'MPElectionYear',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'MemberId',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        put_data()

    except Exception as err:
        print(err)
