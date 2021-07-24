import json
import logging
from datetime import timedelta
from typing import Tuple, List, Dict, Set

import dateutil.parser
import requests

from divisions.month_with_intervals import MonthWithIntervals

URL_SEARCH_DIVISIONS = 'https://commonsvotes-api.parliament.uk/data/divisions.json/search'
DATES_MEM0 = set()


def increment_date(old_date: str, dates_memo: Set[str]) -> str:
    """
    Division datetime is used as a range key in the database. The time portion
    sometimes gets defaulted to midnight in the source data, resulting in duplicate keys.
    This workaround ensures all datetimes are unique.
    """

    if old_date not in dates_memo:
        return old_date

    old_date_str = dateutil.parser.parse(old_date)
    incremented_date = old_date_str + timedelta(seconds=1)
    return increment_date(incremented_date.strftime("%Y-%m-%dT%H:%M:%S%z"), dates_memo)


def get_fields_of_interest(division: dict) -> dict:
    current_date = division['Date']
    current_date = increment_date(current_date, DATES_MEM0)
    DATES_MEM0.add(current_date)

    # TODO: create division object
    return {
        'DivisionId': division['DivisionId'],
        'Date': current_date,
        'Title': division['Title'],
        'AyeCount': division['AyeCount'],
        'NoCount': division['NoCount']
    }


def get_divisions(intervals: MonthWithIntervals) -> List[Dict]:
    DATES_MEM0.clear()

    def make_requests() -> List[Dict]:
        downloaded_divisions = []
        for interval in intervals.get_interval_list:
            params = {'queryParameters.startDate': interval.open, 'queryParameters.endDate': interval.close}
            res = requests.get(URL_SEARCH_DIVISIONS, params)

            if res.status_code != 200:
                error = "failed to download interval: {interval}".format(interval=interval)
                logging.error(error)
                raise RuntimeError(error)

            downloaded_divisions += [get_fields_of_interest(div) for div in json.loads(res.text)]

        return downloaded_divisions

    divisions = make_requests()
    logging.info('processed %s divisions', len(divisions))

    return divisions
