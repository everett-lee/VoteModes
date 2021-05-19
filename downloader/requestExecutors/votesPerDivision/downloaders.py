import concurrent
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Set, Dict

import requests

from votesPerDivision.multithreaded.time_it import timeit

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

    logging.info('downloading division with id', division_id)

    res = requests.get(url)
    while failed_count <= 10 and res.status_code != 200:
        failed_count += 1
        res = requests.get(url)

    if failed_count >= 10:
        error = 'failed to download division with votes with URL {url}'.format(url=url)
        logging.error(error)
        raise RuntimeError(error)

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
