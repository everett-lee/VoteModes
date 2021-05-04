import requests
import json

TOTAL_MPS = 650
URL_GET_DIVISION = 'https://commonsvotes-api.parliament.uk/data/division/'


def get_division_votes_and_id(division: dict, mp_list: set) -> dict:
    ayes = set(map(lambda x: x['MemberId'], division['Ayes']))
    noes = set(map(lambda x: x['MemberId'], division['Noes']))

    no_attend = mp_list.difference(ayes.union(noes))
    # TODO UNIT TEST THIS

    return {
        'DivisionId': division['DivisionId'],
        'Ayes': ayes,
        'Noes': noes,
        'DidNotAttend': no_attend,
        'NotPresent': []
    }


def has_good_attendance(division: dict) -> dict:
    return division['AyeCount'] + division['NoCount'] > TOTAL_MPS * 0.6


def download_votes_per_division() -> None:
    mp_ids = []

    with open('raw/rawMPList', 'r') as raw_mps:
        mp_list = json.loads(raw_mps.read())['Data']
        mp_ids = [mp['MemberId'] for mp in mp_list]

    with open('raw/rawDivisions', 'r') as raw_divisions:
        divisions = raw_divisions.read()
        parsed_json = json.loads(divisions)['Data']

        with_good_attendance = [div for div in parsed_json if has_good_attendance(div)]

        for i in range(1):
            print(with_good_attendance[i])
            division_id = with_good_attendance[i]['DivisionId']
            url = '{base_url}{division_id}.json'.format(base_url=URL_GET_DIVISION, division_id=division_id)
            raw_json = json.loads(requests.get(url).text)
            division_with_votes = get_division_votes_and_id(raw_json, set(mp_ids))

            print(division_with_votes)
