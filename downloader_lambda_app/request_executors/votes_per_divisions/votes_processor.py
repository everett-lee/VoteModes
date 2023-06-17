import logging
from collections import defaultdict
from typing import Dict, List, Set, Union

from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import Table

from ..boto3_helpers.client_wrapper import get_table
from ..divisions.schemas import Division
from .downloaders import VotesDownloader
from .schemas import DivisionWithVotes

VoteIdToVoteMap = Dict[str, Union[str, int]]
MPIdToVotesMap = Dict[int, VoteIdToVoteMap]


class VotesProcessor:
    def __init__(self, votes_downloader: VotesDownloader, mps_table: Table):
        self.votes_downloader = votes_downloader
        self.mps_table = mps_table

    def download_votes_per_division(
        self, divisions: List[Division], election_year: int
    ) -> None:
        total_mps = 650  # not strictly true
        good_attendance_percentage = 0.6

        def has_good_attendance(division: Division) -> bool:
            return division.aye_count + division.no_count > (
                total_mps * good_attendance_percentage
            )

        mp_ids = self._get_mp_ids(self.mps_table, election_year)
        with_good_attendance = [div for div in divisions if has_good_attendance(div)]

        divisions_with_votes = (
            self.votes_downloader.download_all_divisions_with_votes_async(
                with_good_attendance, mp_ids
            )
        )

        assert len(with_good_attendance) == len(divisions_with_votes)

        mps_to_votes = self._map_divisions_with_votes_to_mps(
            divisions_with_votes, mp_ids
        )

        self._set_votes(
            mps_to_votes=mps_to_votes,
            mps_table=self.mps_table,
            election_year=election_year,
        )

    def _map_divisions_with_votes_to_mps(
        self, divisions_with_votes: List[DivisionWithVotes], mp_ids: Set[int]
    ) -> MPIdToVotesMap:
        """
        Takes a list of DivisionWithVotes and a set of MP ids.
        Returns a dict of MP ids mapped to a dict of each division ID and the MP's
        vote for that division
        """

        mps_to_votes = defaultdict(dict)

        for division in divisions_with_votes:
            division_id = division.division_id
            for aye_voter_id in division.ayes:
                mps_to_votes[aye_voter_id][division_id] = "Aye"
            for no_voted_id in division.noes:
                mps_to_votes[no_voted_id][division_id] = "No"
            for no_attend_id in division.no_attends:
                mps_to_votes[no_attend_id][division_id] = "NoAttend"

        # only include mps recorded in the database
        return {
            mp_id: votes for mp_id, votes in mps_to_votes.items() if mp_id in mp_ids
        }

    def _get_mp_ids(self, mps_table: Table, election_year: int) -> Set[int]:
        """
        Gets all MP ids stored in the DynamoDB
        """

        mp_ids_request = mps_table.query(
            KeyConditionExpression=Key("MPElectionYear").eq(election_year),
            ProjectionExpression="MemberId",
        )
        items = mp_ids_request["Items"]

        while "LastEvaluatedKey" in mp_ids_request:
            if mp_ids_request["ResponseMetadata"]["HTTPStatusCode"] != 200:
                logging.error("Failure when fetching MP ids")

            mp_ids_request = mps_table.query(
                KeyConditionExpression=Key("MPElectionYear").eq(election_year),
                ProjectionExpression="MemberId",
                ExclusiveStartKey=mp_ids_request["LastEvaluatedKey"],
            )
            items += mp_ids_request["Items"]

        return {int(item["MemberId"]) for item in items}

    def _get_duplicate_ids(
        self, mp_id: int, list_votes: List[VoteIdToVoteMap], election_year: int
    ) -> Set[int]:
        """ "
        Find IDs for already processed votes
        """
        new_vote_ids = {int(vote["DivisionId"]) for vote in list_votes}

        existing_votes_request = self.mps_table.query(
            KeyConditionExpression=Key("MPElectionYear").eq(election_year)
            & Key("MemberId").eq(mp_id),
            ProjectionExpression="Votes",
        )

        if existing_votes_request["ResponseMetadata"]["HTTPStatusCode"] != 200:
            logging.error("Failed to validate votes for mp with id %s", mp_id)
        else:
            if not existing_votes_request["Items"][0]:
                # Case where no votes present
                return set()

            existing_votes = existing_votes_request["Items"][0]["Votes"]
            existing_vote_ids = {int(vote["DivisionId"]) for vote in existing_votes}

            duplicate_ids = existing_vote_ids.intersection(new_vote_ids)

            if len(duplicate_ids) > 0:
                logging.error(
                    "Votes with these ids have already been processed: %s",
                    duplicate_ids,
                )

            return duplicate_ids

    def _set_votes(
        self, mps_to_votes: MPIdToVotesMap, election_year: int, mps_table: Table
    ) -> None:
        """
        Takes dict mapping each MP ID to the corresponding votes. These votes (mappings from
        divisionId -> Aye/No/NoAttend) are iterated over, already-processed vote IDs
        are removed, and the list of votes for each MP is updated.
        """

        for mp_id, votes in mps_to_votes.items():
            list_votes = [
                {"DivisionId": div_id, "Vote": vote} for (div_id, vote) in votes.items()
            ]
            duplicate_ids = self._get_duplicate_ids(
                mp_id=mp_id, list_votes=list_votes, election_year=election_year
            )
            filtered_list_votes = [
                vote_pair
                for vote_pair in list_votes
                if (int(vote_pair["DivisionId"]) not in duplicate_ids)
            ]

            update_mp_votes_request = mps_table.update_item(
                Key={"MPElectionYear": election_year, "MemberId": int(mp_id)},
                UpdateExpression="SET Votes = list_append(Votes, :new_votes)",
                ExpressionAttributeValues={
                    ":new_votes": filtered_list_votes,
                },
                ReturnValues="UPDATED_NEW",
            )

            if update_mp_votes_request["ResponseMetadata"]["HTTPStatusCode"] != 200:
                logging.error("failed to update votes for mp with id %s", mp_id)
