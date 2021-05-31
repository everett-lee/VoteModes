import os
from datetime import date

from .request_executors.boto3_helpers.client_wrapper import get_queue
from .request_executors.divisions.divisions_list_downloader import download_divisions_list
from .request_executors.votes_per_divisions.vote_per_division_downloader import \
    download_votes_per_division


def lambda_handler(event, context):
    QUEUE_URL = os.getenv('QUEUE_URL')

    today = date.today()
    year = today.year
    month = today.month - 1

    divisions = download_divisions_list(year=year, month=month, election_year=2019)
    download_votes_per_division(divisions=divisions)

    queue = get_queue(QUEUE_URL)
    queue.send_message(
        MessageBody='Processed divisions for {month} {year}'.format(month=month, year=year)
    )
    return 'Success!'

