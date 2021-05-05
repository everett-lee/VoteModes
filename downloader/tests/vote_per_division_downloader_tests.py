from unittest import TestCase
from ..requestExecutors.vote_per_division_downloader import get_division_votes_and_id

mp_ids = {172, 4212, 4057, 39, 140, 4362}

division = {
    "DivisionId": -1,
    "Ayes": [
        {
            "MemberId": 39,
            "Name": "John Whittingdale",
            "Party": "Conservative",
            "SubParty": None,
            "PartyColour": "0000ff",
            "PartyAbbreviation": "Con",
            "MemberFrom": "Maldon",
            "ListAs": "Whittingdale, Mr John",
            "ProxyName": "Stuart Andrew"
        },
        {
            "MemberId": 140,
            "Name": "Margaret Hodge",
            "Party": "Labour",
            "SubParty": None,
            "PartyColour": "ff0000",
            "PartyAbbreviation": "Lab",
            "MemberFrom": "Barking",
            "ListAs": "Hodge, Dame Margaret",
            "ProxyName": "Alan Campbell"
        },
    ],
    "Noes": [
        {
            "MemberId": 4362,
            "Name": "Edward Argar",
            "Party": "Conservative",
            "SubParty": None,
            "PartyColour": "0000ff",
            "PartyAbbreviation": "Con",
            "MemberFrom": "Charnwood",
            "ListAs": "Argar, Edward",
            "ProxyName": "Stuart Andrew"
        },
        {
            "MemberId": 4212,
            "Name": "Debbie Abrahams",
            "Party": "Labour",
            "SubParty": None,
            "PartyColour": "ff0000",
            "PartyAbbreviation": "Lab",
            "MemberFrom": "Oldham East and Saddleworth",
            "ListAs": "Abrahams, Debbie",
            "ProxyName": "Alan Campbell"
        },
    ]
}


class TestGetDivisionVotesAndId(TestCase):
    def test_get_division_votes_and_id(self):
        division_with_votes = get_division_votes_and_id(division, mp_ids)

        self.assertEqual(division_with_votes['DivisionId'], -1)
        self.assertEqual(division_with_votes['Ayes'], {39, 140})
        self.assertEqual(division_with_votes['Noes'], {4362, 4212})
        self.assertEqual(division_with_votes['DidNotAttend'], {4057, 172})
