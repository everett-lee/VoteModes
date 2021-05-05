import requests
import json
from typing import Tuple, List, Set, Dict

TOTAL_MPS = 650
URL_GET_DIVISION = 'https://commonsvotes-api.parliament.uk/data/division/'


def get_division_votes_and_id(division: Dict, mp_ids: Set[int]) -> Dict:
    ayes = set(map(lambda x: x['MemberId'], division['Ayes']))
    noes = set(map(lambda x: x['MemberId'], division['Noes']))
    no_attend = mp_ids.difference(ayes.union(noes))

    return {
        'DivisionId': division['DivisionId'],
        'Ayes': ayes,
        'Noes': noes,
        'DidNotAttend': no_attend,
    }


def get_division_with_votes(division_id: int, mp_ids: Set[int], division_with_votes: List[Dict]) -> List[Dict]:
    url = '{base_url}{division_id}.json'.format(base_url=URL_GET_DIVISION, division_id=division_id)
    raw_json = json.loads(requests.get(url).text)
    return division_with_votes + [get_division_votes_and_id(raw_json, mp_ids)]

def download_votes_per_division() -> None:
    def has_good_attendance(division: dict) -> dict:
        return division['AyeCount'] + division['NoCount'] > TOTAL_MPS * 0.6

    mp_ids = []
    divisions_with_votes = []

    with open('raw/rawMPList', 'r') as raw_mps:
        mp_list = json.loads(raw_mps.read())['Data']
        mp_ids = [int(mp['MemberId']) for mp in mp_list]

    with open('raw/rawDivisions2021', 'r') as raw_divisions:
        divisions = raw_divisions.read()
        parsed_json = json.loads(divisions)['Data']

        with_good_attendance = [div for div in parsed_json if has_good_attendance(div)]

        for i in range(1):
            division_id = with_good_attendance[i]['DivisionId']
            url = '{base_url}{division_id}.json'.format(base_url=URL_GET_DIVISION, division_id=division_id)
            raw_json = json.loads(requests.get(url).text)
            division_with_votes = division_with_votes + get_division_votes_and_id(raw_json, set(mp_ids))
