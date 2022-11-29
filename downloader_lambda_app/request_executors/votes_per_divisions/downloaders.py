import concurrent
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Set

import requests

from ..divisions.division import Division
from .division_with_votes import DivisionWithVotes
from .multithreaded.time_it import timeit

URL_GET_DIVISION = "https://commonsvotes-api.parliament.uk/data/division/"


def get_division_with_votes(division: Dict, mp_ids: Set[int]) -> DivisionWithVotes:
    ayes = {int(vote["MemberId"]) for vote in division["Ayes"]}
    noes = {int(vote["MemberId"]) for vote in division["Noes"]}
    no_attend = mp_ids.difference(ayes.union(noes))

    return DivisionWithVotes(
        division_id=division["DivisionId"],
        ayes=list(ayes),
        noes=list(noes),
        no_attends=list(no_attend),
    )


def download_division_with_vote(
    division_id: int, mp_ids: Set[int]
) -> DivisionWithVotes:
    url = "{base_url}{division_id}.json".format(
        base_url=URL_GET_DIVISION, division_id=division_id
    )
    failed_count = 0

    logging.info("downloading division with id %s", division_id)

    res = requests.get(url)
    while failed_count <= 10 and res.status_code != 200:
        failed_count += 1
        res = requests.get(url)

    if failed_count >= 10:
        error = "failed to download division with votes with URL {url}".format(url=url)
        logging.error(error)
        raise RuntimeError(error)

    json_dict = json.loads(res.text)
    return get_division_with_votes(json_dict, mp_ids)


@timeit
def download_all_divisions_with_votes_sync(
    with_good_attendance: List[Division], mp_ids: Set[int]
) -> List[DivisionWithVotes]:

    division_ids = [division.division_id for division in with_good_attendance]
    return [
        download_division_with_vote(division_id, mp_ids) for division_id in division_ids
    ]


@timeit
def download_all_divisions_with_votes_async(
    with_good_attendance: List[Division], mp_ids: Set[int]
) -> List[DivisionWithVotes]:

    division_ids = [division.division_id for division in with_good_attendance]
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(download_division_with_vote, division_id, mp_ids)
            for division_id in division_ids
        ]

        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    return results
