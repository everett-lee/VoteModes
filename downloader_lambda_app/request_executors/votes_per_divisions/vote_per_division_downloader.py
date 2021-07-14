import logging
from collections import defaultdict
from typing import List, Set, Dict

from boto3.dynamodb.conditions import Key

from .downloaders import download_all_divisions_with_votes_async
from ..boto3_helpers.client_wrapper import get_table

TOTAL_MPS = 650


def map_divisions_with_votes_to_mps(divisions_with_votes: List[Dict], mp_ids: Set[int]) -> Dict:
    mps_to_votes = defaultdict(dict)

    for division in divisions_with_votes:
        division_id = int(division['DivisionId'])
        for aye_voter_id in division['Ayes']:
            mps_to_votes[int(aye_voter_id)][division_id] = 'Aye'
        for no_voted_id in division['Noes']:
            mps_to_votes[int(no_voted_id)][division_id] = 'No'
        for no_attend_id in division['DidNotAttend']:
            mps_to_votes[int(no_attend_id)][division_id] = 'NoAttend'

    # only include mps recorded in the database
    return {id: votes for id, votes in mps_to_votes.items() if id in mp_ids}


def get_mp_ids(mps_table: object) -> Set[int]:
    dynamodb_mp_ids = mps_table.scan(
        ProjectionExpression='MemberId',
    )['Items']

    if not dynamodb_mp_ids:
        logging.info('unable to fetch mp ids from database')

    return set(map(lambda x: int(x['MemberId']), dynamodb_mp_ids))


def set_votes(mps_to_votes: Dict, mps_table: object) -> None:
    def validate_incoming_votes(mp_id: int, list_votes: List) -> Set[int]:
        new_vote_ids = {int(vote['DivisionId']) for vote in list_votes}

        res = mps_table.query(
            KeyConditionExpression=Key('MPElectionYear').eq(2019) & Key('MemberId').eq(mp_id),
            ProjectionExpression='MemberId, Votes'
        )

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            logging.error('Failed to validate votes for mp with id', mp_id)
        else:
            existing_votes = res['Items'][0]['Votes']
            existing_vote_ids = {int(vote['DivisionId']) for vote in existing_votes}

            duplicate_ids = existing_vote_ids.intersection(new_vote_ids)

            if len(duplicate_ids) > 0:
                logging.error('Votes with these ids have been processed already: ', duplicate_ids)

            return duplicate_ids

    for mp_id, votes in mps_to_votes.items():
        list_votes = [{'DivisionId': div_id, 'Vote': vote} for (div_id, vote) in votes.items()]
        existing_votes = validate_incoming_votes(mp_id, list_votes)
        filtered_list_votes = [vote_pair for vote_pair in list_votes
                               if (vote_pair['DivisionId'] not in existing_votes)]

        res = mps_table.update_item(
            Key={
                'MPElectionYear': 2019,
                'MemberId': int(mp_id)
            },
            UpdateExpression="SET Votes = list_append(Votes, :new_votes)",
            ExpressionAttributeValues={
                ':new_votes': filtered_list_votes,
            },
            ReturnValues="UPDATED_NEW"
        )

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            logging.error('failed to update votes for mp with id', mp_id)


def download_votes_per_division(divisions: List[Dict]) -> None:
    def has_good_attendance(division: dict) -> dict:
        return division['AyeCount'] + division['NoCount'] > (TOTAL_MPS * 0.6)

    mps_table = get_table('MPs')

    mp_ids = get_mp_ids(mps_table)

    with_good_attendance = [div for div in divisions if has_good_attendance(div)]

    divisions_with_votes = download_all_divisions_with_votes_async(with_good_attendance, mp_ids)

    assert (len(with_good_attendance) == len(divisions_with_votes))

    mps_to_votes = map_divisions_with_votes_to_mps(divisions_with_votes, mp_ids)
    set_votes(mps_to_votes, mps_table)
