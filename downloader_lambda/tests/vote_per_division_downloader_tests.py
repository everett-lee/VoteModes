import json
from unittest import TestCase, mock

from downloader.request_exectuors.votes_per_divisions.downloaders import download_division_with_vote
from downloader.request_exectuors.votes_per_divisions.downloaders import get_division_votes_and_id
from .data import get_divisions_with_votes_first
from .mock_response_helper.mock_response_helper import get_mock_response

mp_ids = {172, 4212, 4057, 39, 140, 4362}

division = get_divisions_with_votes_first()[0]

class TestGetDivisionVotesAndId(TestCase):
    def test_get_division_votes_and_id(self):
        division_with_votes = get_division_votes_and_id(division, mp_ids)

        self.assertEqual(division_with_votes['DivisionId'], -1)
        self.assertEqual(set(division_with_votes['Ayes']), {172, 4057, 39})
        self.assertEqual(set(division_with_votes['Noes']), {140, 4362})
        self.assertEqual(set(division_with_votes['DidNotAttend']), {4212})

    @mock.patch('requests.get')
    def test_download_division_with_vote_all_failures(self, mock_get):
        mock_response = get_mock_response(status=500)
        mock_get.return_value = mock_response
        with self.assertRaises(RuntimeError):
            download_division_with_vote(-1, mp_ids)

    @mock.patch('requests.get')
    def test_download_division_with_vote_two_failures(self, mock_get):
        mock_response_failed = get_mock_response(status=500)
        mock_response_success = get_mock_response(status=200, text=json.dumps(division))
        mock_get.side_effect = [mock_response_failed, mock_response_failed, mock_response_success]
        result = download_division_with_vote(-1, mp_ids)

        self.assertEqual(result['DivisionId'], -1)
        self.assertEqual(set(result['Ayes']), {172, 4057, 39})
        self.assertEqual(set(result['Noes']), {140, 4362})
        self.assertEqual(set(result['DidNotAttend']), {4212})

