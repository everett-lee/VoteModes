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

        all_mps = table.scan()

        print(all_mps)
        print("hello")

        # for mp_id, votes in mps_to_votes.items():
        #     table.put_item(
        #         Item={
        #             'MemberId': int(mp_id),
        #             'Votes': votes,
        #         }
        #     )


put_data()