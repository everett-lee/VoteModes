from divsions_list_downloader import download_divisions_list

def run_download():
    divisions = download_divisions_list(2021, 5, 2019)

if __name__ == '__main__':
    # download_divisions_list_file_based()
    # divsions_list_downloader.download_divisions_list(2021, 5)
    # mp_list_downloader.download_active_mp_list()
    # vote_per_division_downloader.download_votes_per_division([])
    run_download()


