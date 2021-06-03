import json
import logging

import boto3
import os

AWS_PROFILE = os.getenv('AWS_PROFILE')
TABLE_NAME = 'Divisions'
dynamodb_resource = None

if (AWS_PROFILE == 'localstack'):
    print('Starting load divisions with localstack')
    dynamodb_resource = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                                  endpoint_url='http://localhost:4566')

elif (AWS_PROFILE == 'votemodes'):
    print('Starting load divisions with votemodes')
    dynamodb_resource = boto3.resource('dynamodb')

else:
    print("AWS profile: {profile} is not valid".format(profile=AWS_PROFILE))


def put_data(divisions_table):
    with open('../downloader_lambda_app/raw/rawDivisions', 'r') as raw_2019_2021:
        divisions = json.load(raw_2019_2021)['Data']

        for division in divisions:
            division_id = division['DivisionId']
            date = division['Date'].strip()
            title = division['Title'].strip()
            aye_count = division['AyeCount']
            no_count = division['NoCount']

            divisions_table.put_item(
                Item={
                    'DivisionElectionYear': 2019,
                    'DivisionId': division_id,
                    'DivisionDate': date,
                    'Title': title,
                    'AyeCount': aye_count,
                    'NoCount': no_count,
                }
            )


if dynamodb_resource:
    divisions_table = dynamodb_resource.Table(TABLE_NAME)
    print('Putting divisons table data')
    put_data(divisions_table)
else:
    print('No dynamodb resource')
