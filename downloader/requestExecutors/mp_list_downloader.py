import json
import requests

URL_GET_MPS_BASE = 'http://data.parliament.uk/membersdataplatform/services/mnis/members/'
URL_GET_MPS_QUERY = 'query/House=Commons%7CIsEligible=true%7Ccommonsmemberbetween={start_date}and{end_date}/'
START_DATE = '2019-12-15'
END_DATE = '2021-05-03'


def get_fields_of_interest(mp: dict) -> dict:
    return {
        'MemberId': int(mp['@Member_Id']),
        'Name': mp['DisplayAs']
    }


def download_active_mp_list() -> None:
    full_url = URL_GET_MPS_BASE + URL_GET_MPS_QUERY.format(start_date=START_DATE, end_date=END_DATE)
    headers = {'content-type': 'application/json'}
    mp_results = requests.get(full_url, headers=headers)

    with open('raw/temp', 'w') as f:
        f.write(mp_results.text)

    with open('raw/temp', 'r', encoding='utf-8-sig') as f:
        parsed_json = json.load(f)

    all_members = parsed_json['Members']['Member']
    members_with_id_and_name = [get_fields_of_interest(mp) for mp in all_members]

    with open('raw/rawMPList', 'w') as raw_json:
        raw_json.write('{"Data": ')
        raw_json.write(json.dumps(members_with_id_and_name))
        raw_json.write('}')
