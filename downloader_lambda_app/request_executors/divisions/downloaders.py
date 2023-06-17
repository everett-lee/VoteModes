import json
import logging
from typing import List, Optional

import requests
from mypy_boto3_dynamodb.service_resource import Table

from .schemas import Division, MonthWithIntervals


class DivisionDownloader:
    def __init__(self, divisions_table: Table, divisions_url: Optional[str] = None):
        if divisions_url:
            self.divisions_url = divisions_url
        else:
            self.divisions_url = (
                "https://commonsvotes-api.parliament.uk/data/divisions.json/search"
            )
        self.divisions_table = divisions_table

        # a store of datetimes used to find and increment duplicates
        self.saved_dates = set()

    def _create_division(self, division: dict) -> Division:
        """
        :param division: Parsed Dict of JSON representation of a Division
        :param saved_dates: A maintained set of dates seen so far. Used to remove duplicates
        :return: a constructed Division
        """

        date = division["Date"].strip()
        self.saved_dates.add(date)

        return Division(division, self.saved_dates)

    def _get_divisions(self, intervals: MonthWithIntervals) -> List[Division]:
        """
        :param intervals: the three intervals of the month (with start and end date) to query
        :return: a list of Divisions
        """

        def make_requests() -> List[Division]:
            downloaded_divisions = []

            for interval in intervals.get_interval_list:
                params = {
                    "queryParameters.startDate": interval.open,
                    "queryParameters.endDate": interval.close,
                }
                res = requests.get(self.divisions_url, params)

                if res.status_code != 200:
                    error = f"failed to download interval: {interval}, status code {res.status_code}"
                    logging.error(error)
                    raise RuntimeError(error)

                downloaded_divisions += [
                    self._create_division(div) for div in json.loads(res.text)
                ]

            return downloaded_divisions

        divisions = make_requests()
        logging.info("processed %s divisions", len(divisions))

        return divisions

    def download_divisions_list(
        self, year: int, month: int, election_year: int, put_to_table: bool = True
    ) -> List[Division]:
        intervals = MonthWithIntervals(year=year, month=month)
        divisions = self._get_divisions(intervals)
        logging.info("Downloaded %s divisions", divisions)

        if put_to_table:
            logging.info(f"Putting {len(divisions)} to Divisions table")
            for division in divisions:
                res = self.divisions_table.put_item(
                    Item={
                        "DivisionElectionYear": election_year,
                        "DivisionId": division.division_id,
                        "DivisionDate": division.date,
                        "Title": division.title,
                        "AyeCount": division.aye_count,
                        "NoCount": division.no_count,
                    }
                )

                if res["ResponseMetadata"]["HTTPStatusCode"] != 200:
                    logging.error("failed to put division", division, "to database")

        return divisions
