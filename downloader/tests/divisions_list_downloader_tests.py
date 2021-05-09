from ..requestExecutors.divsions_list_downloader import get_date_intervals
from ..requestExecutors.divsions_list_downloader import get_fields_of_interest

from unittest import TestCase

division = {"DivisionId": 1025,
            "Date": "2021-04-28T16:54:00",
            "PublicationUpdated": "2021-04-28T17:32:43",
            "Number": 283,
            "IsDeferred": False,
            "EVELType": "",
            "EVELCountry": "",
            "Title": "National Security and Investment Bill: motion to disagree with Lords Amendments 11B and 11C",
            "AyeCount": 358,
            "NoCount": 269,
            "DoubleMajorityAyeCount": None,
            "DoubleMajorityNoCount": None,
            "AyeTellers": [],
            "NoTellers": [],
            "Ayes": [],
            "Noes": [],
            "FriendlyDescription": None,
            "FriendlyTitle": None,
            "NoVoteRecorded": [],
            "RemoteVotingStart": None,
            "RemoteVotingEnd": None
            }


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
        self.assertEqual(foi['DivisionId'], 1025)
        self.assertEqual(foi['Date'], '2021-04-28')
        self.assertEqual(foi['Title'], 'National Security and Investment Bill: motion to disagree with Lords Amendments 11B and 11C')
        self.assertEqual(foi['AyeCount'], 358)
        self.assertEqual(foi['NoCount'], 269)