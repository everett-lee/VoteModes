import json
import boto3
import os

AWS_PROFILE = os.getenv('AWS_PROFILE')
TABLE_NAME = 'Divisions2019'
dynamodb = None

if (AWS_PROFILE == 'localstack'):
    dynamodb = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                         endpoint_url='http://localhost:4566')
else:
    print("AWS profile: {profile} is not valid".format(profile=AWS_PROFILE))


def put_data():
    with open('../downloader/raw/rawDivisions2019-2020', 'r') as raw_2019_2020:
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
                    'Date': date,
                    'Title': title,
                    'AyeCount': aye_count,
                    'NoCount': no_count,
                }
            )

    with open('../downloader/raw/rawDivisions2021', 'r') as raw_2019_2020:
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
                    'Date': date,
                    'Title': title,
                    'AyeCount': aye_count,
                    'NoCount': no_count,
                }
            )


if dynamodb:
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'DivisionId',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'Date',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'DivisionId',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'Date',
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