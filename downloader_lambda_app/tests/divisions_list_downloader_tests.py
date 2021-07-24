from datetime import datetime
from unittest import TestCase, mock

from divisions.month_with_intervals import MonthWithIntervals
from data_loader import get_divisions_first
from mock_response_helper.mock_response_helper import get_mock_response
from request_executors.divisions.downloaders import get_fields_of_interest, get_divisions, increment_date

division = get_divisions_first()[0]

class TestGetDateIntervals(TestCase):
    def test_jan_interval_has_correct_range(self):
        intervals = MonthWithIntervals(month=1, year=1999).get_interval_list

        self.assertEqual(intervals[0].open, '1999-01-01')
        self.assertEqual(intervals[0].close, '1999-01-10')
        self.assertEqual(intervals[1].open, '1999-01-11')
        self.assertEqual(intervals[1].close, '1999-01-20')
        self.assertEqual(intervals[2].open, '1999-01-21')
        self.assertEqual(intervals[2].close, '1999-02-01')

    def test_feb_interval_has_correct_range(self):
        intervals = MonthWithIntervals(month=2, year=1999).get_interval_list

        self.assertEqual(intervals[0].open, '1999-02-02')
        self.assertEqual(intervals[0].close, '1999-02-10')
        self.assertEqual(intervals[1].open, '1999-02-11')
        self.assertEqual(intervals[1].close, '1999-02-20')
        self.assertEqual(intervals[2].open, '1999-02-21')
        self.assertEqual(intervals[2].close, '1999-03-01')

    def test_dec_interval_has_correct_range(self):
        intervals = MonthWithIntervals(month=12, year=1999).get_interval_list

        self.assertEqual(intervals[0].open, '1999-12-02')
        self.assertEqual(intervals[0].close, '1999-12-10')
        self.assertEqual(intervals[1].open, '1999-12-11')
        self.assertEqual(intervals[1].close, '1999-12-20')
        self.assertEqual(intervals[2].open, '1999-12-21')
        self.assertEqual(intervals[2].close, '1999-12-31')

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
        intervals = MonthWithIntervals(month=12, year=1999)
        mock_get.return_value = mock_response
        with self.assertRaises(RuntimeError):
            get_divisions(intervals)

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
