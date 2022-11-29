import logging
import sys
from typing import List

from ..boto3_helpers.client_wrapper import get_table
from .division import Division
from .downloaders import get_divisions
from .month_with_intervals import MonthWithIntervals

TABLE_NAME = "Divisions"


def download_divisions_list(
    year: int, month: int, election_year: int
) -> List[Division]:
    intervals = MonthWithIntervals(year=year, month=month)
    divisions = get_divisions(intervals)
    logging.info("Downloaded %s divisions", divisions)
    table = get_table(TABLE_NAME)

    for division in divisions:

        res = table.put_item(
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
