from ..requestExecutors.divsions_list_downloader import get_date_intervals

from unittest import TestCase


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
