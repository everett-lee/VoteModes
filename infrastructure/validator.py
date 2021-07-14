from typing import List, Set, Dict
import boto3
from boto3.dynamodb.conditions import Key

dynamodb_client = boto3.resource('dynamodb')
mps = dynamodb_client.Table('MPs')

res = mps.query(
    KeyConditionExpression=Key('MPElectionYear').eq(2019) & Key('MemberId').eq(1583),
    ProjectionExpression='MemberId, Votes'
)

votes = res['Items'][0]['Votes']
vote_ids = {int(vote['DivisionId']) for vote in votes}
print(vote_ids)