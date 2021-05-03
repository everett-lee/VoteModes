import requests
import json

from divsions_list_downloader import download_divisions_list
from mp_list_downloader import download_active_mp_list

TOTAL_MPS = 650
URL_GET_DIVISION = 'https://commonsvotes-api.parliament.uk/data/division/'

def download_votes_per_division() -> None:
    def get_division_votes_and_id(division: dict) -> dict:
        ayes = list(map(lambda x: x['MemberId'], division['Ayes']))
        noes = list(map(lambda x: x['MemberId'], division['Noes']))

        # TODO: ADD HAVE NOT VOTED

        return {
            'DivisionId': division['DivisionId'],
            'Ayes': ayes,
            'Noes': noes,
            'NotPresent': []
        }

    def has_good_attendance(division: dict) -> dict:
        return division['AyeCount'] + division['NoCount'] > TOTAL_MPS * 0.6

    with open('./raw/rawDivisions', 'r') as rawJSon:
        res = rawJSon.read()
        parsed_json = json.loads(res)["Data"]

        with_good_attendance = [div for div in parsed_json if has_good_attendance(div)]

        for i in range(1):
            print(with_good_attendance[i])
            division_id = with_good_attendance[i]['DivisionId']
            url = '{base_url}{division_id}.json'.format(base_url=URL_GET_DIVISION, division_id=division_id)
            raw_json = json.loads(requests.get(url).text)
            division_with_votes = get_division_votes_and_id(raw_json)

            print(division_with_votes)


def getit() -> None:
    #download_divisions_list()
    #download_votes_per_division()
    download_active_mp_list()