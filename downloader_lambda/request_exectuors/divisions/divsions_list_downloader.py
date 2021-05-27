import logging
from typing import List, Dict

from downloader.request_exectuors.boto3_helpers.client_wrapper import get_table
from downloader.request_exectuors.divisions.downloaders import get_date_intervals, get_divisions

TABLE_NAME = 'Divisions'


def download_divisions_list(year: int, month: int, election_year: int) -> List[Dict]:
    intervals = get_date_intervals(year, month)
    divisions = get_divisions(intervals)
    table = get_table(TABLE_NAME)

    for division in divisions:
        division_id = division['DivisionId']
        date = division['Date'].strip()
        title = division['Title'].strip()
        aye_count = division['AyeCount'],
        no_count = division['NoCount']

        res = table.put_item(
            Item={
                'DivisionElectionYear': election_year,
                'DivisionId': division_id,
                'DivisionDate': date,
                'Title': title,
                'AyeCount': aye_count,
                'NoCount': no_count
            }
        )

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            logging.error('failed to put division', division, 'to database')

    return divisions
