import logging
import os
import sys
from datetime import date

from request_executors.boto3_helpers.client_wrapper import get_queue
from request_executors.divisions.downloaders import (
    DivisionDownloader,
)
from request_executors.votes_per_divisions.vote_per_division_downloader import (
    download_votes_per_division,
)

sys.path.append(os.path.join(os.path.dirname(__file__)))
logging.getLogger().setLevel(logging.INFO)


def handler(event, context):
    queue_url = os.getenv("QUEUE_URL")
    # Must be manually set on deployment
    election_year = int(os.getenv("ELECTION_YEAR"))

    today = date.today()
    year = today.year
    # get data for previous month
    month = today.month - 1

    divisions_downloader = DivisionDownloader(dynamo_table_name="Divisions")
    divisions = divisions_downloader.download_divisions_list(
        year=year, month=month, election_year=election_year
    )
    download_votes_per_division(divisions=divisions, election_year=election_year)

    queue = get_queue(queue_url)
    queue.send_message(
        MessageBody="Processed divisions for {month}-{year}".format(
            month=month, year=year
        )
    )
    return "Success!"
