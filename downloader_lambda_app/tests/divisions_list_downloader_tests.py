from datetime import datetime
from unittest import TestCase, mock

from ..request_executors.divisions.divisions_list_downloader import get_date_intervals
from ..request_executors.divisions.downloaders import get_fields_of_interest, get_divisions, increment_date
from .data import get_divisions_first
from .mock_response_helper.mock_response_helper import get_mock_response

division = get_divisions_first()[0]


class TestGetDateIntervals(TestCase):
    def test_jan_interval_has_correct_range(self):
        interval = get_date_intervals(1999, 1)
        self.assertEqual(interval[0][0], '1999-01-01')
        self.assertEqual(interval[0][1], '1999-01-10')
        self.assertEqual(interval[1][0], '1999-01-11')
        self.assertEqual(interval[1][1], '1999-01-20')
        self.assertEqual(interval[2][0], '1999-01-21')
        self.assertEqual(interval[2][1], '1999-02-01')

    def test_feb_interval_has_correct_range(self):
        interval = get_date_intervals(1999, 2)
        self.assertEqual(interval[0][0], '1999-02-02')
        self.assertEqual(interval[0][1], '1999-02-10')
        self.assertEqual(interval[1][0], '1999-02-11')
        self.assertEqual(interval[1][1], '1999-02-20')
        self.assertEqual(interval[2][0], '1999-02-21')
        self.assertEqual(interval[2][1], '1999-03-01')

    def test_dec_interval_has_correct_range(self):
        interval = get_date_intervals(1999, 12)
        self.assertEqual(interval[0][0], '1999-12-02')
        self.assertEqual(interval[0][1], '1999-12-10')
        self.assertEqual(interval[1][0], '1999-12-11')
        self.assertEqual(interval[1][1], '1999-12-20')
        self.assertEqual(interval[2][0], '1999-12-21')
        self.assertEqual(interval[2][1], '1999-12-31')

    def test_get_fields_of_interest(self):
        foi = get_fields_of_interest(division)
        self.assertEqual(foi['DivisionId'], -1)
        self.assertEqual(foi['Date'], '2021-04-28T16:54:00')
        self.assertEqual(foi['Title'],
                         'National Security and Investment Bill: motion to disagree with Lords Amendments 11B and 11C')
        self.assertEqual(foi['AyeCount'], 358)
        self.assertEqual(foi['NoCount'], 269)

    @mock.patch('requests.get')
    def test_download_division_with_vote_all_failures(self, mock_get):
        mock_response = get_mock_response(status=500)
        interval = get_date_intervals(1999, 12)
        mock_get.return_value = mock_response
        with self.assertRaises(RuntimeError):
            get_divisions(interval)

    def test_increment_date_empty_set(self):
        mock_dates_memo = set()
        input_date = datetime(2021, 5, 17, 11, 59, 59).strftime("%Y-%m-%dT%H:%M:%S%z")
        updated = increment_date(input_date, mock_dates_memo)

        self.assertEqual(updated, '2021-05-17T11:59:59')

    def test_increment_date_one_date_clash(self):
        mock_dates_memo = {'2021-05-17T11:59:59'}
        input_date = datetime(2021, 5, 17, 11, 59, 59).strftime("%Y-%m-%dT%H:%M:%S%z")
        updated = increment_date(input_date, mock_dates_memo)

        self.assertEqual(updated, '2021-05-17T12:00:00')

    def test_increment_date_two_date_clashes(self):
        mock_dates_memo = {'2021-05-17T11:59:59', '2021-05-17T12:00:00'}
        input_date = datetime(2021, 5, 17, 11, 59, 59).strftime("%Y-%m-%dT%H:%M:%S%z")
        updated = increment_date(input_date, mock_dates_memo)

        self.assertEqual(updated, '2021-05-17T12:00:01')

    def test_increment_date_one_date_clash_one_unrelated(self):
        mock_dates_memo = {'2021-05-17T11:59:59', '2021-06-17T12:20:00'}
        input_date = datetime(2021, 5, 17, 11, 59, 59).strftime("%Y-%m-%dT%H:%M:%S%z")
        updated = increment_date(input_date, mock_dates_memo)

        self.assertEqual(updated, '2021-05-17T12:00:00')