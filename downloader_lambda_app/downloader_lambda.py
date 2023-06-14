import logging
import os
import sys
from datetime import date

from request_executors.boto3_helpers.client_wrapper import get_queue
from request_executors.divisions.downloaders import DivisionDownloader
from request_executors.votes_per_divisions.downloaders import VotesDownloader
from request_executors.votes_per_divisions.votes_processor import \
    VotesProcessor

sys.path.append(os.path.join(os.path.dirname(__file__)))
logging.getLogger().setLevel(logging.INFO)

def run(year: int, month: int) -> None:
    queue_url = os.getenv("QUEUE_URL", "")
    # Must be manually set on deployment
    election_year = int(os.getenv("ELECTION_YEAR"))

    logging.info(f"Running Lambda for {year}-{month}")
    divisions_downloader = DivisionDownloader(dynamo_table_name="Divisions")
    votes_downloader = VotesDownloader()
    votes_processor = VotesProcessor(
        votes_downloader=votes_downloader, mps_table_name="MPs"
    )

    divisions = divisions_downloader.download_divisions_list(
        year=year, month=month, election_year=election_year
    )
    votes_processor.download_votes_per_division(
        divisions=divisions, election_year=election_year
    )

    if queue_url:
        logging.info(f"Writing to queue at URL {queue_url}")
        queue = get_queue(queue_url)
        queue.send_message(
            MessageBody="Processed divisions for {month}-{year}".format(
                month=month, year=year
            )
        )

def handler(event, context):
    today = date.today()
    year = today.year
    # get data for previous month
    month = today.month - 1
    run(year, month)

    return "Success!"