import json
from unittest import TestCase, mock

from votesPerDivision.downloaders import download_division_with_vote
from votesPerDivision.downloaders import get_division_votes_and_id
from .data import get_divisions_with_votes
from .mock_response_helper.mock_response_helper import get_mock_response

mp_ids = {172, 4212, 4057, 39, 140, 4362}

division = get_divisions_with_votes()[0]

class TestGetDivisionVotesAndId(TestCase):
    def test_get_division_votes_and_id(self):
        division_with_votes = get_division_votes_and_id(division, mp_ids)

        self.assertEqual(division_with_votes['DivisionId'], -1)
        self.assertEqual(set(division_with_votes['Ayes']), {39, 140})
        self.assertEqual(set(division_with_votes['Noes']), {4362, 4212})
        self.assertEqual(set(division_with_votes['DidNotAttend']), {4057, 172})

    @mock.patch('requests.get')
    def test_download_division_with_vote_all_failures(self, mock_get):
        mock_response = get_mock_response(status=500)
        mock_get.return_value = mock_response
        result = download_division_with_vote(-1, mp_ids)

        self.assertEqual(result['last_failure_code'], 500)
        self.assertGreaterEqual(result['times_called'], 10)

    @mock.patch('requests.get')
    def test_download_division_with_vote_two_failures(self, mock_get):
        mock_response_failed = get_mock_response(status=500)
        mock_response_success = get_mock_response(status=200, text=json.dumps(division))
        mock_get.side_effect = [mock_response_failed, mock_response_failed, mock_response_success]
        result = download_division_with_vote(-1, mp_ids)

        self.assertEqual(result['DivisionId'], -1)
        self.assertGreaterEqual(set(result['Ayes']), {39, 140})
        self.assertGreaterEqual(set(result['Noes']), {4362, 4212})
        self.assertGreaterEqual(set(result['DidNotAttend']), {4057, 172})

