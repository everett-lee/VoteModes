from requestExecutors import divsions_list_downloader
from requestExecutors import mp_list_downloader
from requestExecutors import vote_per_division_downloader

if __name__ == '__main__':
    divsions_list_downloader.download_divisions_list(5)
    #mp_list_downloader.download_active_mp_list()
    #vote_per_division_downloader.download_votes_per_division()
