import os

from boto3Helpers.client_wrapper import get_queue
from divisions.divsions_list_downloader import download_divisions_list
from votesPerDivision.vote_per_division_downloader import download_votes_per_division
from datetime import date

def lambda_handler(event, context):
    QUEUE_URL = os.getenv('QUEUE_URL')

    today = date.today()
    year = today.year
    month = today.month

    divisions = download_divisions_list(year=year, month=month, election_year=2019)
    download_votes_per_division(divisions=divisions)

    queue = get_queue(QUEUE_URL)
    queue.send_message(
        MessageBody='Processed divisions for {month} {year}'.format(month=month, year=year)
    )
    return 'Success!'

