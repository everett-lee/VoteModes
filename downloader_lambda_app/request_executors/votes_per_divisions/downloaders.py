import concurrent
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Set

import requests

from ..divisions.schemas import Division
from .schemas import DivisionWithVotes
from .timer.time_it import timeit


class VotesDownloader:
    def __init__(self, votes_base_url: Optional[str] = None):
        if votes_base_url:
            self.votes_base_url = votes_base_url
        else:
            self.votes_base_url = (
                "https://commonsvotes-api.parliament.uk/data/division/"
            )

    def _get_division_with_votes(
        self, division: Dict, mp_ids: Set[int]
    ) -> DivisionWithVotes:
        ayes = {int(vote["MemberId"]) for vote in division["Ayes"]}
        noes = {int(vote["MemberId"]) for vote in division["Noes"]}
        no_attend = mp_ids.difference(ayes.union(noes))

        return DivisionWithVotes(
            division_id=int(division["DivisionId"]),
            ayes=list(ayes),
            noes=list(noes),
            no_attends=list(no_attend),
        )

    def _download_division_with_vote(
        self, division_id: int, mp_ids: Set[int]
    ) -> DivisionWithVotes:
        url = f"{self.votes_base_url}{division_id}.json"

        failed_count = 0
        logging.info("downloading division with id %s", division_id)

        res = requests.get(url)
        while failed_count <= 10 and res.status_code != 200:
            logging.info(f"Retrying fetch of Division wth id {division_id}")
            failed_count += 1
            res = requests.get(url)

        if failed_count >= 10:
            error = "failed to download division with votes with URL {url}".format(
                url=url
            )
            logging.error(error)
            raise RuntimeError(error)

        json_dict = json.loads(res.text)
        return self._get_division_with_votes(json_dict, mp_ids)

    @timeit
    def download_all_divisions_with_votes_sync(
        self, with_good_attendance: List[Division], mp_ids: Set[int]
    ) -> List[DivisionWithVotes]:

        division_ids = [division.division_id for division in with_good_attendance]
        return [
            self._download_division_with_vote(division_id, mp_ids)
            for division_id in division_ids
        ]

    @timeit
    def download_all_divisions_with_votes_async(
        self, with_good_attendance: List[Division], mp_ids: Set[int]
    ) -> List[DivisionWithVotes]:

        division_ids = [division.division_id for division in with_good_attendance]
        results = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self._download_division_with_vote, division_id, mp_ids)
                for division_id in division_ids
            ]

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        return results
