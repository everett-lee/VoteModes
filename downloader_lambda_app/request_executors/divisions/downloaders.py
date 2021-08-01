import json
import logging
from typing import List

import requests

from divisions.division import Division
from divisions.month_with_intervals import MonthWithIntervals

URL_SEARCH_DIVISIONS = 'https://commonsvotes-api.parliament.uk/data/divisions.json/search'


def create_division(div: dict, saved_dates: set) -> Division:
    date = div['Date'].strip()
    saved_dates.add(date)

    return Division(div, saved_dates)


def get_divisions(intervals: MonthWithIntervals) -> List[Division]:
    def make_requests() -> List[Division]:
        downloaded_divisions = []
        saved_dates = set()
        for interval in intervals.get_interval_list:
            params = {'queryParameters.startDate': interval.open, 'queryParameters.endDate': interval.close}
            res = requests.get(URL_SEARCH_DIVISIONS, params)

            if res.status_code != 200:
                error = "failed to download interval: {interval}".format(interval=interval)
                logging.error(error)
                raise RuntimeError(error)

            downloaded_divisions += [create_division(div, saved_dates) for div in json.loads(res.text)]

        return downloaded_divisions

    divisions = make_requests()
    logging.info('processed %s divisions', len(divisions))

    return divisions
