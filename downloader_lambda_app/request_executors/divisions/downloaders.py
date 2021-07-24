import json
import logging
from datetime import timedelta
from typing import Tuple, List, Dict, Set

import requests

from divisions.division import Division
from divisions.month_with_intervals import MonthWithIntervals

URL_SEARCH_DIVISIONS = 'https://commonsvotes-api.parliament.uk/data/divisions.json/search'


def get_divisions(intervals: MonthWithIntervals) -> List[Division]:
    def make_requests() -> List[Division]:
        downloaded_divisions = []
        for interval in intervals.get_interval_list:
            params = {'queryParameters.startDate': interval.open, 'queryParameters.endDate': interval.close}
            res = requests.get(URL_SEARCH_DIVISIONS, params)

            if res.status_code != 200:
                error = "failed to download interval: {interval}".format(interval=interval)
                logging.error(error)
                raise RuntimeError(error)

            downloaded_divisions += [Division(div) for div in json.loads(res.text)]

        return downloaded_divisions

    divisions = make_requests()
    logging.info('processed %s divisions', len(divisions))

    return divisions
