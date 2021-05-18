import json
import os
from unittest import TestCase, mock

import boto3

from data import get_divisions_first
from data import get_divisions_second
from data import get_divisions_with_votes_first
from data import get_divisions_with_votes_second
from data import get_mps
from downloader.main import run_download
from downloader.tests.mock_response_helper.mock_response_helper import get_mock_response


@mock.patch.dict(os.environ, {'AWS_PROFILE': 'localstack'})
class IntegrationTests(TestCase):
    dynamodb = None

    def assert_using_localstack(self):
        self.assertEqual(os.getenv('AWS_PROFILE'), 'localstack')

    @mock.patch('requests.get')
    def test_full_process(self, mock_get):
        self.assert_using_localstack()
        self.delete_tables()
        [divisions_table, mps_table] = self.create_tables()
        self.load_mps(mps_table)

        mock_divisions_with_votes_first = get_divisions_with_votes_first()
        mock_divisions_with_votes_second = get_divisions_with_votes_second()
        mock_response_first_divisions = get_mock_response(status=200, text=json.dumps(get_divisions_first()))
        mock_response_second_divisions = get_mock_response(status=200, text=json.dumps(get_divisions_second()))
        mock_response_empty = get_mock_response(status=200, text=json.dumps([]))
        mock_response_divisions_with_votes_1 = get_mock_response(status=200,
                                                                 text=json.dumps(mock_divisions_with_votes_first[0]))
        mock_response_divisions_with_votes_2 = get_mock_response(status=200,
                                                                 text=json.dumps(mock_divisions_with_votes_first[1]))
        mock_response_divisions_with_votes_3 = get_mock_response(status=200,
                                                                 text=json.dumps(mock_divisions_with_votes_second[0]))

        mock_get.side_effect = [mock_response_first_divisions, mock_response_empty, mock_response_empty,
                                mock_response_divisions_with_votes_1, mock_response_divisions_with_votes_2,
                                mock_response_second_divisions, mock_response_empty, mock_response_empty,
                                mock_response_divisions_with_votes_3]
        run_download()

        saved_divisions = self.scan_table(divisions_table)['Items']
        self.assertEqual(len(saved_divisions), 2)

        division_ids = set(map(lambda x: int(x['DivisionId']), saved_divisions))
        self.assertEqual(division_ids, {-1, -2})

        saved_mps = self.scan_table(mps_table)['Items']
        for mp in saved_mps:
            self.assertEqual(len(mp['Votes']), 2)

        mps_as_map = {int(mp['MemberId']): mp for mp in saved_mps}
        self.assertEqual(len(mps_as_map), 6)
        self.assertVotes(mps_as_map[172]['Votes'], 'Aye', 'No', None)
        self.assertVotes(mps_as_map[4057]['Votes'], 'Aye', 'NoAttend', None)
        self.assertVotes(mps_as_map[39]['Votes'], 'Aye', 'Aye', None)
        self.assertVotes(mps_as_map[140]['Votes'], 'No', 'Aye', None)
        self.assertVotes(mps_as_map[4362]['Votes'], 'No', 'No', None)
        self.assertVotes(mps_as_map[4212]['Votes'], 'NoAttend', 'NoAttend', None)

        # second run
        run_download()

        saved_divisions = self.scan_table(divisions_table)['Items']
        self.assertEqual(len(saved_divisions), 3)

        division_ids = set(map(lambda x: int(x['DivisionId']), saved_divisions))
        self.assertEqual(division_ids, {-1, -2, -3})

        saved_mps = self.scan_table(mps_table)['Items']
        for mp in saved_mps:
            self.assertEqual(len(mp['Votes']), 3)

        mps_as_map = {int(mp['MemberId']): mp for mp in saved_mps}
        self.assertEqual(len(mps_as_map), 6)
        self.assertVotes(mps_as_map[172]['Votes'], 'Aye', 'No', 'Aye')
        self.assertVotes(mps_as_map[4057]['Votes'], 'Aye', 'NoAttend', 'Aye')
        self.assertVotes(mps_as_map[39]['Votes'], 'Aye', 'Aye', 'Aye')
        self.assertVotes(mps_as_map[140]['Votes'], 'No', 'Aye', 'No')
        self.assertVotes(mps_as_map[4362]['Votes'], 'No', 'No', 'No')
        self.assertVotes(mps_as_map[4212]['Votes'], 'NoAttend', 'NoAttend', 'NoAttend')

    def assertVotes(self, mp_votes, first_vote, second_vote, third_vote):
        self.assertEqual(mp_votes[0]['Vote'], first_vote)
        self.assertEqual(mp_votes[1]['Vote'], second_vote)

        if (third_vote):
            self.assertEqual(mp_votes[2]['Vote'], third_vote)

    def create_tables(self):
        divisions_table = mps_table = None
        try:
            divisions_table = self.get_dynamodb().create_table(
                TableName='Divisions',
                KeySchema=[
                    {
                        'AttributeName': 'DivisionElectionYear',
                        'KeyType': 'HASH',
                    },
                    {
                        'AttributeName': 'DivisionDate',
                        'KeyType': 'RANGE',
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'DivisionElectionYear',
                        'AttributeType': 'N'
                    },
                    {
                        'AttributeName': 'DivisionDate',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

        except Exception as err:
            print(err)

        try:
            mps_table = self.get_dynamodb().create_table(
                TableName='MPs',
                KeySchema=[
                    {
                        'AttributeName': 'MPElectionYear',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'MemberId',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'MPElectionYear',
                        'AttributeType': 'N'
                    },
                    {
                        'AttributeName': 'MemberId',
                        'AttributeType': 'N'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

        except Exception as err:
            print(err)

        return [divisions_table, mps_table]

    def load_mps(self, mps_table):
        mps = get_mps()

        for mp in mps:
            member_id = mp['MemberId']
            name = mp['Name']

            mps_table.put_item(
                Item={
                    'MPElectionYear': 2019,
                    'MemberId': member_id,
                    'Name': name,
                    'Votes': []
                }
            )

    def delete_tables(self):
        divisions_table = self.get_dynamodb().Table('Divisions')
        mps_table = self.get_dynamodb().Table('MPs')

        try:
            divisions_table.delete()
            mps_table.delete()
        except Exception as err:
            print(err)

    def scan_table(self, table):
        return table.scan()

    def get_dynamodb(self):
        if os.getenv('AWS_PROFILE') == 'localstack' and self.dynamodb is None:
            self.dynamodb = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                                      endpoint_url='http://localhost:4566')
        return self.dynamodb
