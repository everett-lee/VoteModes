import json


def get_divisions_first():
    with open('data/first_divisions.json', 'r') as file:
        return json.loads(file.read())


get_divisions_first()


def get_divisions_second():
    return [
        {
            "DivisionId": -3,
            "Date": "2021-05-28T16:20:00",
            "PublicationUpdated": "2021-05-28T16:20:00",
            "Number": 444,
            "IsDeferred": False,
            "EVELType": "",
            "EVELCountry": "",
            "Title": "Give Lee free money bill",
            "AyeCount": 358,
            "NoCount": 269,
            "DoubleMajorityAyeCount": None,
            "DoubleMajorityNoCount": None,
            "AyeTellers": [
                {
                    "MemberId": 4033,
                    "Name": "David Rutley",
                    "Party": "Conservative",
                    "SubParty": None,
                    "PartyColour": "0000ff",
                    "PartyAbbreviation": "Con",
                    "MemberFrom": "Macclesfield",
                    "ListAs": "Rutley, David",
                    "ProxyName": None
                },
                {
                    "MemberId": 3992,
                    "Name": "James Morris",
                    "Party": "Conservative",
                    "SubParty": None,
                    "PartyColour": "0000ff",
                    "PartyAbbreviation": "Con",
                    "MemberFrom": "Halesowen and Rowley Regis",
                    "ListAs": "Morris, James",
                    "ProxyName": None
                }
            ],
            "NoTellers": [
                {
                    "MemberId": 4378,
                    "Name": "Colleen Fletcher",
                    "Party": "Labour",
                    "SubParty": None,
                    "PartyColour": "ff0000",
                    "PartyAbbreviation": "Lab",
                    "MemberFrom": "Coventry North East",
                    "ListAs": "Fletcher, Colleen",
                    "ProxyName": None
                },
                {
                    "MemberId": 4610,
                    "Name": "Bambos Charalambous",
                    "Party": "Labour",
                    "SubParty": None,
                    "PartyColour": "ff0000",
                    "PartyAbbreviation": "Lab",
                    "MemberFrom": "Enfield, Southgate",
                    "ListAs": "Charalambous, Bambos",
                    "ProxyName": None
                }
            ],
            "Ayes": [],
            "Noes": [],
            "FriendlyDescription": None,
            "FriendlyTitle": None,
            "NoVoteRecorded": [],
            "RemoteVotingStart": None,
            "RemoteVotingEnd": None
        }
    ]


def get_mps():
    return [
        {
            "MemberId": 172,
            "Name": "Ms Ada Lovelace"
        },
        {
            "MemberId": 4212,
            "Name": "Mr Charlie Day"
        },
        {
            "MemberId": 4057,
            "Name": "Ms Dina Mite"
        },
        {
            "MemberId": 39,
            "Name": "Mr Stephen Morrissey"
        },
        {
            "MemberId": 140,
            "Name": "Captain Ahab"
        },
        {
            "MemberId": 4362,
            "Name": "Mr Mason Mount"
        }
    ]


def get_divisions_with_votes_first():
    return [{
        "DivisionId": -1,
        "Date": "2020-01-09T17:10:00",
        "PublicationUpdated": "2020-01-09T17:34:11",
        "Number": 14,
        "IsDeferred": False,
        "EVELType": "",
        "EVELCountry": "",
        "Title": "National Security and Investment Bill: motion to disagree with Lords Amendments 11B and 11C",
        "AyeCount": 330,
        "NoCount": 231,
        "DoubleMajorityAyeCount": None,
        "DoubleMajorityNoCount": None,
        "AyeTellers": [
            {
                "MemberId": 4369,
                "Name": "Tom Pursglove",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Corby",
                "ListAs": "Pursglove, Tom",
                "ProxyName": None
            },
            {
                "MemberId": 3992,
                "Name": "James Morris",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Halesowen and Rowley Regis",
                "ListAs": "Morris, James",
                "ProxyName": None
            }
        ],
        "NoTellers": [
            {
                "MemberId": 4456,
                "Name": "Jeff Smith",
                "Party": "Labour",
                "SubParty": None,
                "PartyColour": "ff0000",
                "PartyAbbreviation": "Lab",
                "MemberFrom": "Manchester, Withington",
                "ListAs": "Smith, Jeff",
                "ProxyName": None
            },
            {
                "MemberId": 4617,
                "Name": "Matt Western",
                "Party": "Labour",
                "SubParty": None,
                "PartyColour": "ff0000",
                "PartyAbbreviation": "Lab",
                "MemberFrom": "Warwick and Leamington",
                "ListAs": "Western, Matt",
                "ProxyName": None
            }
        ],
        "Ayes": [
            {
                "MemberId": 172,
                "Name": "Ms Ada Lovelace",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Maidenhead",
                "ListAs": "Ms Ada Lovelace",
                "ProxyName": None
            },
            {
                "MemberId": 4057,
                "Name": "Ms Dina Mite",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Colchester",
                "ListAs": "Ms Dina Mite",
                "ProxyName": None
            },
            {
                "MemberId": 39,
                "Name": "Mr Stephen Morrissey",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Wokingham",
                "ListAs": "Mr Stephen Morrissey",
                "ProxyName": None
            }
        ],
        "Noes": [
            {
                "MemberId": 140,
                "Name": "Captain Ahab",
                "Party": "Labour",
                "SubParty": None,
                "PartyColour": "ff0000",
                "PartyAbbreviation": "Lab",
                "MemberFrom": "Hayes and Harlington",
                "ListAs": "Captain Ahab",
                "ProxyName": None
            },
            {
                "MemberId": 4362,
                "Name": "Mr Mason Mount",
                "Party": "Labour",
                "SubParty": None,
                "PartyColour": "ff0000",
                "PartyAbbreviation": "Lab",
                "MemberFrom": "Leyton and Wanstead",
                "ListAs": "Mr Mason Mount",
                "ProxyName": "Lampard's Son"
            }
        ],
        "RemoteVotingStart": None,
        "RemoteVotingEnd": None
    },
        {
            "DivisionId": -2,
            "Date": "2020-01-09T17:10:00",
            "PublicationUpdated": "2020-01-09T17:34:11",
            "Number": 14,
            "IsDeferred": False,
            "EVELType": "",
            "EVELCountry": "",
            "Title": "Motion to revoke: Immigration (Guidance on Detention of Vulnerable Persons) Regulations 2021 (SI 2021 No. 184)",
            "AyeCount": 330,
            "NoCount": 231,
            "DoubleMajorityAyeCount": None,
            "DoubleMajorityNoCount": None,
            "AyeTellers": [
                {
                    "MemberId": 4369,
                    "Name": "Tom Pursglove",
                    "Party": "Conservative",
                    "SubParty": None,
                    "PartyColour": "0000ff",
                    "PartyAbbreviation": "Con",
                    "MemberFrom": "Corby",
                    "ListAs": "Pursglove, Tom",
                    "ProxyName": None
                },
                {
                    "MemberId": 3992,
                    "Name": "James Morris",
                    "Party": "Conservative",
                    "SubParty": None,
                    "PartyColour": "0000ff",
                    "PartyAbbreviation": "Con",
                    "MemberFrom": "Halesowen and Rowley Regis",
                    "ListAs": "Morris, James",
                    "ProxyName": None
                }
            ],
            "NoTellers": [
                {
                    "MemberId": 4456,
                    "Name": "Jeff Smith",
                    "Party": "Labour",
                    "SubParty": None,
                    "PartyColour": "ff0000",
                    "PartyAbbreviation": "Lab",
                    "MemberFrom": "Manchester, Withington",
                    "ListAs": "Smith, Jeff",
                    "ProxyName": None
                },
                {
                    "MemberId": 4617,
                    "Name": "Matt Western",
                    "Party": "Labour",
                    "SubParty": None,
                    "PartyColour": "ff0000",
                    "PartyAbbreviation": "Lab",
                    "MemberFrom": "Warwick and Leamington",
                    "ListAs": "Western, Matt",
                    "ProxyName": None
                }
            ],
            "Ayes": [
                {
                    "MemberId": 39,
                    "Name": "Mr Stephen Morrissey",
                    "Party": "Conservative",
                    "SubParty": None,
                    "PartyColour": "0000ff",
                    "PartyAbbreviation": "Con",
                    "MemberFrom": "Wokingham",
                    "ListAs": "Mr Stephen Morrissey",
                    "ProxyName": None
                },
                {
                    "MemberId": 140,
                    "Name": "Captain Ahab",
                    "Party": "Labour",
                    "SubParty": None,
                    "PartyColour": "ff0000",
                    "PartyAbbreviation": "Lab",
                    "MemberFrom": "Hayes and Harlington",
                    "ListAs": "Captain Ahab",
                    "ProxyName": None
                }
            ],
            "Noes": [
                {
                    "MemberId": 172,
                    "Name": "Ms Ada Lovelace",
                    "Party": "Conservative",
                    "SubParty": None,
                    "PartyColour": "0000ff",
                    "PartyAbbreviation": "Con",
                    "MemberFrom": "Maidenhead",
                    "ListAs": "Ms Ada Lovelace",
                    "ProxyName": None
                },
                {
                    "MemberId": 4362,
                    "Name": "Mr Mason Mount",
                    "Party": "Labour",
                    "SubParty": None,
                    "PartyColour": "ff0000",
                    "PartyAbbreviation": "Lab",
                    "MemberFrom": "Leyton and Wanstead",
                    "ListAs": "Mr Mason Mount",
                    "ProxyName": "Lampard's Son"
                }
            ],
            "RemoteVotingStart": None,
            "RemoteVotingEnd": None
        }
    ]


def get_divisions_with_votes_second():
    return [{
        "DivisionId": -3,
        "Date": "2021-05-28T16:20:00",
        "PublicationUpdated": "2021-05-28T16:20:00",
        "Number": 444,
        "IsDeferred": False,
        "EVELType": "",
        "EVELCountry": "",
        "Title": "Give Lee free money bill",
        "AyeCount": 358,
        "NoCount": 269,
        "DoubleMajorityAyeCount": None,
        "DoubleMajorityNoCount": None,
        "AyeTellers": [
            {
                "MemberId": 4369,
                "Name": "Tom Pursglove",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Corby",
                "ListAs": "Pursglove, Tom",
                "ProxyName": None
            },
            {
                "MemberId": 3992,
                "Name": "James Morris",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Halesowen and Rowley Regis",
                "ListAs": "Morris, James",
                "ProxyName": None
            }
        ],
        "NoTellers": [
            {
                "MemberId": 4456,
                "Name": "Jeff Smith",
                "Party": "Labour",
                "SubParty": None,
                "PartyColour": "ff0000",
                "PartyAbbreviation": "Lab",
                "MemberFrom": "Manchester, Withington",
                "ListAs": "Smith, Jeff",
                "ProxyName": None
            },
            {
                "MemberId": 4617,
                "Name": "Matt Western",
                "Party": "Labour",
                "SubParty": None,
                "PartyColour": "ff0000",
                "PartyAbbreviation": "Lab",
                "MemberFrom": "Warwick and Leamington",
                "ListAs": "Western, Matt",
                "ProxyName": None
            }
        ],
        "Ayes": [
            {
                "MemberId": 172,
                "Name": "Ms Ada Lovelace",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Maidenhead",
                "ListAs": "Ms Ada Lovelace",
                "ProxyName": None
            },
            {
                "MemberId": 4057,
                "Name": "Ms Dina Mite",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Colchester",
                "ListAs": "Ms Dina Mite",
                "ProxyName": None
            },
            {
                "MemberId": 39,
                "Name": "Mr Stephen Morrissey",
                "Party": "Conservative",
                "SubParty": None,
                "PartyColour": "0000ff",
                "PartyAbbreviation": "Con",
                "MemberFrom": "Wokingham",
                "ListAs": "Mr Stephen Morrissey",
                "ProxyName": None
            }
        ],
        "Noes": [
            {
                "MemberId": 140,
                "Name": "Captain Ahab",
                "Party": "Labour",
                "SubParty": None,
                "PartyColour": "ff0000",
                "PartyAbbreviation": "Lab",
                "MemberFrom": "Hayes and Harlington",
                "ListAs": "Captain Ahab",
                "ProxyName": None
            },
            {
                "MemberId": 4362,
                "Name": "Mr Mason Mount",
                "Party": "Labour",
                "SubParty": None,
                "PartyColour": "ff0000",
                "PartyAbbreviation": "Lab",
                "MemberFrom": "Leyton and Wanstead",
                "ListAs": "Mr Mason Mount",
                "ProxyName": "Lampard's Son"
            }
        ],
        "RemoteVotingStart": None,
        "RemoteVotingEnd": None
    }
    ]
