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
        mp_dict = {}

        for mp in mps:
            mp['Votes'] = {}
            mp_dict[str(mp["MemberId"])] = mp

        table.put_item(
            Item={
                'MPElectionYear': 2019,
                'MPData': mp_dict,
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
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'MPElectionYear',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 500,
                'WriteCapacityUnits': 500
            }
        )

        put_data()

    except Exception as err:
        print(err)