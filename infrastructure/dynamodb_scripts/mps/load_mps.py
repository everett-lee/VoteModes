import json
import boto3
import os

AWS_PROFILE = os.getenv('AWS_PROFILE')
TABLE_NAME = 'MPs'
dynamodb_resource = None

if (AWS_PROFILE == 'localstack'):
    dynamodb_resource = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                                  endpoint_url='http://localhost:4566')

elif (AWS_PROFILE == 'votemodes'):
    print('Starting load MPs with votemodes')
    dynamodb_resource = boto3.resource('dynamodb')


else:
    print("AWS profile: {profile} is not valid".format(profile=AWS_PROFILE))

def put_data(table):
    with open('../downloader_lambda_app/raw/rawMPList', 'r') as rawMps:
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

if dynamodb_resource:
    try:
        table = dynamodb_resource.Table(TABLE_NAME)
        put_data(table)


    except Exception as err:
        print(err)
