import json

from downloader_lambda.request_exectuors.votes_per_divisions.downloaders import download_all_divisions_with_votes_sync
from downloader_lambda.request_exectuors.votes_per_divisions.vote_per_division_downloader import map_divisions_with_votes_to_mps

TOTAL_MPS = 650


def download_votes_per_division_file_based() -> None:
    def has_good_attendance(division: dict) -> dict:
        return division['AyeCount'] + division['NoCount'] > TOTAL_MPS * 0.6

    mp_ids = []
    with_good_attendance = []
    divisions_with_votes = []

    with open('raw/rawMPList', 'r') as raw_mps:
        mp_list = json.loads(raw_mps.read())['Data']
        mp_ids = set([int(mp['MemberId']) for mp in mp_list])

    with open('raw/rawDivisions', 'r') as raw_divisions:
        divisions = raw_divisions.read()
        parsed_json = json.loads(divisions)['Data']

        with_good_attendance = [div for div in parsed_json if has_good_attendance(div)]

    divisions_with_votes = download_all_divisions_with_votes_sync(with_good_attendance, mp_ids)

    assert (len(with_good_attendance) == len(divisions_with_votes))

    with open('raw/rawDivisionsWithVotes', 'w') as raw_divisions_with_votes:
        raw_divisions_with_votes.write('{"Data": ')
        raw_divisions_with_votes.write(json.dumps(divisions_with_votes))
        raw_divisions_with_votes.write('}')

    mps_to_votes = map_divisions_with_votes_to_mps(divisions_with_votes, mp_ids)

    with open('raw/rawMPsToVotes', 'w') as raw_mps_to_votes:
        raw_mps_to_votes.write('{"Data": ')
        raw_mps_to_votes.write(json.dumps(mps_to_votes))
        raw_mps_to_votes.write('}')
