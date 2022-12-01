from datetime import datetime
from unittest import TestCase, mock

from test.data_loader import get_divisions_first
from request_executors.divisions.schemas import Division, MonthWithIntervals
from test.helpers.mock_response_helper import get_mock_response

from request_executors.divisions.downloaders import DivisionDownloader

division_json = get_divisions_first()[0]
division_downloader = DivisionDownloader()


class TestGetDateIntervals(TestCase):
    def test_jan_interval_has_correct_range(self):
        intervals = MonthWithIntervals(month=1, year=1999).get_interval_list

        self.assertEqual(intervals[0].open, "1999-01-01")
        self.assertEqual(intervals[0].close, "1999-01-10")
        self.assertEqual(intervals[1].open, "1999-01-11")
        self.assertEqual(intervals[1].close, "1999-01-20")
        self.assertEqual(intervals[2].open, "1999-01-21")
        self.assertEqual(intervals[2].close, "1999-02-01")

    def test_feb_interval_has_correct_range(self):
        intervals = MonthWithIntervals(month=2, year=1999).get_interval_list

        self.assertEqual(intervals[0].open, "1999-02-02")
        self.assertEqual(intervals[0].close, "1999-02-10")
        self.assertEqual(intervals[1].open, "1999-02-11")
        self.assertEqual(intervals[1].close, "1999-02-20")
        self.assertEqual(intervals[2].open, "1999-02-21")
        self.assertEqual(intervals[2].close, "1999-03-01")

    def test_dec_interval_has_correct_range(self):
        intervals = MonthWithIntervals(month=12, year=1999).get_interval_list

        self.assertEqual(intervals[0].open, "1999-12-02")
        self.assertEqual(intervals[0].close, "1999-12-10")
        self.assertEqual(intervals[1].open, "1999-12-11")
        self.assertEqual(intervals[1].close, "1999-12-20")
        self.assertEqual(intervals[2].open, "1999-12-21")
        self.assertEqual(intervals[2].close, "1999-12-31")

    def test_create_division(self):
        division = Division(division_json, set())
        self.assertEqual(division.division_id, -1)
        self.assertEqual(division.date, "2021-04-28T16:54:00")
        self.assertEqual(
            division.title,
            "National Security and Investment Bill: motion to disagree with Lords Amendments 11B and 11C",
        )
        self.assertEqual(division.aye_count, 358)
        self.assertEqual(division.no_count, 269)

    @mock.patch("requests.get")
    def test_download_division_with_vote_all_failures(self, mock_get):
        mock_response = get_mock_response(status=500)
        intervals = MonthWithIntervals(month=12, year=1999)
        mock_get.return_value = mock_response
        with self.assertRaises(RuntimeError):
            division_downloader._get_divisions(intervals)

    def test_increment_date_empty_set(self):
        division_json["Date"] = datetime(2021, 5, 17, 11, 59, 59).strftime(
            "%Y-%m-%dT%H:%M:%S%z"
        )
        division = Division(division_json, set())
        self.assertEqual(division.date, "2021-05-17T11:59:59")

    def test_increment_date_one_date_clash(self):
        division_json["Date"] = datetime(2021, 5, 17, 11, 59, 59).strftime(
            "%Y-%m-%dT%H:%M:%S%z"
        )
        saved = {"2021-05-17T11:59:59"}
        division = Division(division_json, saved)
        self.assertEqual(division.date, "2021-05-17T12:00:00")

    def test_increment_date_two_date_clashes(self):
        division_json["Date"] = datetime(2021, 5, 17, 11, 59, 59).strftime(
            "%Y-%m-%dT%H:%M:%S%z"
        )
        saved = {"2021-05-17T11:59:59", "2021-05-17T12:00:00"}
        division = Division(division_json, saved)
        self.assertEqual(division.date, "2021-05-17T12:00:01")

    def test_increment_date_one_date_clash_one_unrelated(self):
        division_json["Date"] = datetime(2021, 5, 17, 11, 59, 59).strftime(
            "%Y-%m-%dT%H:%M:%S%z"
        )
        saved = {"2021-05-17T11:59:59", "2021-06-17T12:20:00"}
        division = Division(division_json, saved)
        self.assertEqual(division.date, "2021-05-17T12:00:00")
