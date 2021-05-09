import concurrent
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import requests
import json
from typing import List, Set, Dict

from .multithreaded.time_it import timeit

TOTAL_MPS = 650
URL_GET_DIVISION = 'https://commonsvotes-api.parliament.uk/data/division/'


def get_division_votes_and_id(division: Dict, mp_ids: Set[int]) -> Dict:
    ayes = set(map(lambda x: x['MemberId'], division['Ayes']))
    noes = set(map(lambda x: x['MemberId'], division['Noes']))
    no_attend = mp_ids.difference(ayes.union(noes))

    return {
        'DivisionId': int(division['DivisionId']),
        'Ayes': list(ayes),
        'Noes': list(noes),
        'DidNotAttend': list(no_attend),
    }


def download_division_with_vote(division_id: int, mp_ids: Set[int]) -> Dict:
    url = '{base_url}{division_id}.json'.format(base_url=URL_GET_DIVISION, division_id=division_id)
    failed_count = 0

    print('downloading division with id', division_id)

    res = requests.get(url)
    while failed_count <= 10 and res.status_code != 200:
        failed_count += 1
        res = requests.get(url)

    if failed_count >= 10:
        return {
            'last_failure_code': res.status_code,
            'times_called': failed_count
        }
        # TODO LOG ERROR FETCHING

    raw_json = json.loads(res.text)
    return get_division_votes_and_id(raw_json, mp_ids)


@timeit
def download_all_divisions_with_votes_sync(with_good_attendance: List[Dict], mp_ids: Set[int]) -> List[Dict]:
    division_ids = [division['DivisionId'] for division in with_good_attendance]
    return [download_division_with_vote(division_id, mp_ids) for division_id in division_ids]


@timeit
def download_all_divisions_with_votes_async(with_good_attendance: List[Dict], mp_ids: Set[int]) -> List[Dict]:
    division_ids = [division['DivisionId'] for division in with_good_attendance]
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_division_with_vote, division_id, mp_ids) for division_id in division_ids]

        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    return results


def download_votes_per_division() -> None:
    def has_good_attendance(division: dict) -> dict:
        return division['AyeCount'] + division['NoCount'] > TOTAL_MPS * 0.6

    mp_ids = []
    with_good_attendance = []
    divisions_with_votes = []
    mps_to_votes = defaultdict(dict)

    with open('raw/rawMPList', 'r') as raw_mps:
        mp_list = json.loads(raw_mps.read())['Data']
        mp_ids = set([int(mp['MemberId']) for mp in mp_list])

    with open('raw/rawDivisions', 'r') as raw_divisions:
        divisions = raw_divisions.read()
        parsed_json = json.loads(divisions)['Data']

        with_good_attendance = with_good_attendance + [div for div in parsed_json if has_good_attendance(div)]

    divisions_with_votes = download_all_divisions_with_votes_async(with_good_attendance, mp_ids)

    print(len(with_good_attendance))
    print(len(divisions_with_votes))
    assert (len(with_good_attendance) == len(divisions_with_votes))

    with open('raw/rawDivisionsWithVotes', 'w') as raw_divisions_with_votes:
        raw_divisions.write('{"Data": ')
        raw_divisions.write(json.dumps(divisions_with_votes))
        raw_divisions.write('}')

    for division in divisions_with_votes:
        division_id = int(division['DivisionId'])
        for aye_voter_id in division['Ayes']:
            mps_to_votes[int(aye_voter_id)][division_id] = 'Aye'
        for no_voted_id in division['Noes']:
            mps_to_votes[int(no_voted_id)][division_id] = 'No'
        for no_attend_id in division['DidNotAttend']:
            mps_to_votes[int(no_attend_id)][division_id] = 'NoAttend'

    # only include mps recorded in the database
    with_recorded_mps = {id: votes for id, votes in mps_to_votes.items() if id in mp_ids}

    with open('raw/rawMPsToVotes', 'w') as raw_mps_to_votes:
        raw_mps_to_votes.write('{"Data": ')
        raw_mps_to_votes.write(json.dumps(with_recorded_mps))
        raw_mps_to_votes.write('}')
