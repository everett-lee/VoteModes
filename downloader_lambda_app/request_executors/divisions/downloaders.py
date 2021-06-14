import json
import logging
from datetime import timedelta
from typing import Tuple, List, Dict, Set

import dateutil.parser
import requests

URL_SEARCH_DIVISIONS = 'https://commonsvotes-api.parliament.uk/data/divisions.json/search'
DATES_MEM0 = set()

"""
Date of division is used as a range key in the database, but this appears to get defaulted
to midnight in some cases, resulting in duplicate keys. This workaround ensures all dates 
are unique
"""
def increment_date(old_date: str, dates_memo: Set[str]) -> str:
    if old_date not in dates_memo:
        return old_date

    old_date_str = dateutil.parser.parse(old_date)
    incremented_date = old_date_str + timedelta(seconds=1)
    print('old', old_date, 'new', incremented_date.strftime("%Y-%m-%dT%H:%M:%S%z"))
    return increment_date(incremented_date.strftime("%Y-%m-%dT%H:%M:%S%z"), dates_memo)


def get_fields_of_interest(division: dict) -> dict:
    current_date = division['Date']
    current_date = increment_date(current_date, DATES_MEM0)
    DATES_MEM0.add(current_date)

    return {
        'DivisionId': division['DivisionId'],
        'Date': current_date,
        'Title': division['Title'],
        'AyeCount': division['AyeCount'],
        'NoCount': division['NoCount']
    }


def download_divisions_list_to_file() -> None:
    DATES_MEM0.clear()
    divisions = []

    # 2019
    params = {'queryParameters.startDate': '2019-12-13', 'queryParameters.endDate': '2019-12-31'}
    res = json.loads(requests.get(URL_SEARCH_DIVISIONS, params).text)
    divisions += [get_fields_of_interest(div) for div in res]

    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        intervals = get_date_intervals(2020, month)
        divisions += get_divisions(intervals)

    for month in [1, 2, 3, 4]:
        intervals = get_date_intervals(2021, month)
        divisions += get_divisions(intervals)

    with open('raw/rawDivisions', 'w') as raw_divisions:
        raw_divisions.write('{"Data": ')
        raw_divisions.write(json.dumps(divisions))
        raw_divisions.write('}')


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


def get_divisions(intervals: List[Tuple[str, str]]) -> List[Dict]:
    DATES_MEM0.clear()

    def make_requests() -> List[Dict]:
        downloaded_divisions = []
        for interval in intervals:
            params = {'queryParameters.startDate': interval[0], 'queryParameters.endDate': interval[1]}
            res = requests.get(URL_SEARCH_DIVISIONS, params)

            if res.status_code != 200:
                error = "failed to download interval {interval}".format(interval=interval)
                logging.error(error)
                raise RuntimeError(error)

            downloaded_divisions += [get_fields_of_interest(div) for div in json.loads(res.text)]

        return downloaded_divisions

    divisions = make_requests()
    logging.info('processed %s divisions', len(divisions))

    return divisions
