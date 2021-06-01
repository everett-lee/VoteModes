from downloader_lambda_app.request_executors.divisions.divisions_list_downloader import download_divisions_list
from downloader_lambda_app.request_executors.votes_per_divisions.vote_per_division_downloader import \
    download_votes_per_division


def run_download():
    print('in run download')
    divisions = download_divisions_list(year=2021, month=5, election_year=2019)
    download_votes_per_division(divisions=divisions)


if __name__ == '__main__':
    print('working')
    run_download()
