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

        for mp_id, votes in mps_to_votes.items():
            list_votes = [{"DivisionId": div_id, "Vote": vote} for (div_id, vote) in votes.items()]

            table.update_item(
                Key={
                    'MPElectionYear': 2019,
                    'MemberId': int(mp_id)
                },
                UpdateExpression="SET Votes = list_append(Votes, :new_votes)",
                ExpressionAttributeValues={
                    ':new_votes': list_votes,
                },
                ReturnValues="UPDATED_NEW"
            )


put_data()
