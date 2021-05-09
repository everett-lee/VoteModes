import json
import boto3
import os

AWS_PROFILE = os.getenv('AWS_PROFILE')
TABLE_NAME = 'Divisions2019'
dynamodb_resource = None

if (AWS_PROFILE == 'localstack'):
    dynamodb_resource = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                                  endpoint_url='http://localhost:4566')

else:
    print("AWS profile: {profile} is not valid".format(profile=AWS_PROFILE))


def put_data():
    with open('../downloader/raw/rawDivisions', 'r') as raw_2019_2020:
        divisions = json.load(raw_2019_2020)['Data']

        for division in divisions:
            division_id = division['DivisionId']
            date = division['Date'].strip()
            title = division['Title'].strip()
            aye_count = division['AyeCount']
            no_count = division['NoCount']

            table.put_item(
                Item={
                    'DivisionId': division_id,
                    'VoteDate': date,
                    'Title': title,
                    'AyeCount': aye_count,
                    'NoCount': no_count,
                }
            )


if dynamodb_resource:
    try:
        table = dynamodb_resource.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'DivisionId',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'DivisionId',
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
