import requests
import json
from typing import Tuple, List

URL_SEARCH_DIVISIONS = 'https://commonsvotes-api.parliament.uk/data/divisions.json/search'


def get_fields_of_interest(division: dict) -> dict:
    return {
        'DivisionId': division['DivisionId'],
        'Date': division['Date'],
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
        else '{year}-12-31'

    return [(first_open, first_close), (second_open, second_close), (third_open, third_close)]


def download_divisions_list() -> None:
    with open('../raw/rawDivisions', 'a') as rawJSon:
        rawJSon.write('{"Data": ')

    divisions = []

    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        first_interval, second_interval, third_interval = get_date_intervals(2020, month)

        first_params = {'queryParameters.startDate': first_interval[0], 'queryParameters.endDate': first_interval[1]}
        first_third = requests.get(URL_SEARCH_DIVISIONS, first_params)
        second_params = {'queryParameters.startDate': second_interval[0], 'queryParameters.endDate': second_interval[1]}
        second_third = requests.get(URL_SEARCH_DIVISIONS, second_params)
        third_params = {'queryParameters.startDate': third_interval[0], 'queryParameters.endDate': third_interval[1]}
        third_third = requests.get(URL_SEARCH_DIVISIONS, third_params)

        divisions += [get_fields_of_interest(div) for div in json.loads(first_third.text)]
        divisions += [get_fields_of_interest(div) for div in json.loads(second_third.text)]
        divisions += [get_fields_of_interest(div) for div in json.loads(third_third.text)]

    with open('../raw/rawDivisions', 'a') as rawJSon:
        rawJSon.write(json.dumps(divisions))
        rawJSon.write('}')
