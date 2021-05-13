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
    with open('../downloader/raw/rawMPsToVotes', 'r') as rawMps:
        mps_to_votes = json.load(rawMps)['Data']
        table = dynamodb.Table(TABLE_NAME)

        all_mps = table.get_item(
            Key={'MPElectionYear': 2019}
        )['Item']['MPData']

        for mp_id, votes in mps_to_votes.items():
            mp = all_mps[mp_id]
            mp['Votes'].update(votes)

        table.put_item(
            Item={
                'MPElectionYear': 2019,
                'MPData': all_mps,
            }
        )

put_data()