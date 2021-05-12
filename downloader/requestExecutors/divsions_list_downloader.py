import json
from typing import Tuple, List, Dict

import dateutil.parser
import requests

from .boto3Helpers.client_wrapper import get_table

URL_SEARCH_DIVISIONS = 'https://commonsvotes-api.parliament.uk/data/divisions.json/search'
TABLE_NAME = 'Divisions2019'


def get_fields_of_interest(division: dict) -> dict:
    def datetime_string_to_date_string(datetime_str: str) -> str:
        dt = dateutil.parser.isoparse(datetime_str)
        return str(dt.date())

    return {
        'DivisionId': division['DivisionId'],
        'Date': datetime_string_to_date_string(division['Date']),
        'Title': division['Title'],
        'AyeCount': division['AyeCount'],
        'NoCount': division['NoCount']
    }


# Split the month into three intervals so as not to exceed the maximum number of results
# per request
def get_date_intervals(year: int, month: int) -> List[Tuple[str, str]]:
    def month_to_str(int_month: int) -> str:
        if int_month < 10:
            return "0{month}".format(month=int_month)
        else:
            return "{month}".format(month=int_month)

    first_open = '{year}-{month}-01'.format(year=year, month=month_to_str(month)) if month == 1 \
        else '{year}-{month}-02'.format(year=year, month=month_to_str(month))
    first_close = '{year}-{month}-10'.format(year=year, month=month_to_str(month))

    second_open = '{year}-{month}-11'.format(year=year, month=month_to_str(month))
    second_close = '{year}-{month}-20'.format(year=year, month=month_to_str(month))

    third_open = '{year}-{month}-21'.format(year=year, month=month_to_str(month))
    third_close = '{year}-{month}-01'.format(year=year, month=month_to_str(month + 1)) if month < 12 \
        else '{year}-12-31'.format(year=year)

    return [(first_open, first_close), (second_open, second_close), (third_open, third_close)]


def get_divisions(first_interval: Tuple[str, str], second_interval: Tuple[str, str],
                  third_interval: Tuple[str, str]) -> List[Dict]:
    divisions = []

    first_params = {'queryParameters.startDate': first_interval[0], 'queryParameters.endDate': first_interval[1]}
    first_third = requests.get(URL_SEARCH_DIVISIONS, first_params)
    second_params = {'queryParameters.startDate': second_interval[0], 'queryParameters.endDate': second_interval[1]}
    second_third = requests.get(URL_SEARCH_DIVISIONS, second_params)
    third_params = {'queryParameters.startDate': third_interval[0], 'queryParameters.endDate': third_interval[1]}
    third_third = requests.get(URL_SEARCH_DIVISIONS, third_params)

    if first_third.status_code != 200:
        print(first_params, first_third.status_code)
    if second_third.status_code != 200:
        print(second_params, second_third.status_code)
    if third_third.status_code != 200:
        print(third_params, third_third.status_code)

    divisions += [get_fields_of_interest(div) for div in json.loads(first_third.text)]
    divisions += [get_fields_of_interest(div) for div in json.loads(second_third.text)]
    divisions += [get_fields_of_interest(div) for div in json.loads(third_third.text)]

    print('processed', len(divisions))

    return divisions


def download_divisions_list_file_based() -> None:
    divisions = []

    # 2019
    params = {'queryParameters.startDate': '2019-12-13', 'queryParameters.endDate': '2019-12-31'}
    res = json.loads(requests.get(URL_SEARCH_DIVISIONS, params).text)
    divisions += [get_fields_of_interest(div) for div in res]

    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        first_interval, second_interval, third_interval = get_date_intervals(2020, month)
        divisions += get_divisions(first_interval, second_interval, third_interval)

    for month in [1, 2, 3, 4]:
        first_interval, second_interval, third_interval = get_date_intervals(2021, month)
        divisions += get_divisions(first_interval, second_interval, third_interval)

    with open('raw/rawDivisions', 'w') as raw_divisions:
        raw_divisions.write('{"Data": ')
        raw_divisions.write(json.dumps(divisions))
        raw_divisions.write('}')

def download_divisions_list(year: int, month: int) -> List[Dict]:
    first_interval, second_interval, third_interval = get_date_intervals(year, month)

    divisions = get_divisions(first_interval, second_interval, third_interval)

    table = get_table(TABLE_NAME)

    for division in divisions:
        division_id = division['DivisionId']
        date = division['Date'].strip()
        title = division['Title'].strip()
        aye_count = division['AyeCount'],
        no_count = division['NoCount']

        res = table.put_item(
            Item={
                'DivisionId': division_id,
                'VoteDate': date,
                'Title': title,
                'AyeCount': aye_count,
                'NoCount': no_count
            }
        )

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            None # TODO Log failure

    return divisions
