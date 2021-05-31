from  request_executors.divisions.downloaders import download_divisions_list_to_file


def run_download():
    # divisions = download_divisions_list(year=2021, month=5, election_year=2019)
    # download_votes_per_division(divisions=divisions)

    download_divisions_list_to_file()


if __name__ == '__main__':
    run_download()
