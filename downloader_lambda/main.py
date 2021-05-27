from downloader_lambda.request_exectuors.divisions.divsions_list_downloader import download_divisions_list
from downloader_lambda.request_exectuors.votes_per_divisions.vote_per_division_downloader import download_votes_per_division


def run_download():
    divisions = download_divisions_list(year=2021, month=5, election_year=2019)
    download_votes_per_division(divisions=divisions)



if __name__ == '__main__':
    # download_divisions_list_file_based()
    # divsions_list_downloader.download_divisions_list(2021, 5)
    # mp_list_downloader.download_active_mp_list()
    # vote_per_division_downloader.download_votes_per_division([])
    run_download()
