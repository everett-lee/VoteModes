from request_executors.votes_per_divisions.votes_per_division_file_based import \
    download_votes_per_division_file_based
from request_executors.divisions.downloaders import download_divisions_list_to_file
from request_executors.divisions.divisions_list_downloader import download_divisions_list
from request_executors.votes_per_divisions.vote_per_division_downloader import \
    download_votes_per_division
from request_executors.mps.mp_list_downloader import download_active_mp_list_to_file

def run_download():
    print('in run download')
    # download_active_mp_list_to_file()
    # download_divisions_list_to_file()
    download_votes_per_division_file_based()

    # divisions = download_divisions_list(year=2021, month=5, election_year=2019)
    # download_votes_per_division(divisions=divisions)


if __name__ == '__main__':
    print('working')
    run_download()
