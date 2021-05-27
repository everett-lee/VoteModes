import json
import os
from datetime import date
from unittest import TestCase, mock

import boto3

from data import get_divisions_first
from data import get_divisions_second
from data import get_divisions_with_votes_first
from data import get_divisions_with_votes_second
from data import get_mps
from downloader_lambda.downloader_lambda import lambda_handler
from downloader_lambda.tests.mock_response_helper.mock_response_helper import get_mock_response

localhost_queue_url = "http://localhost:4566/000000000000/LambdaQueue"


@mock.patch.dict(os.environ, {'AWS_PROFILE': 'localstack', 'QUEUE_URL': localhost_queue_url})
class IntegrationTests(TestCase):
    dynamodb = None
    sqs = None

    def assert_using_localstack(self):
        self.assertEqual(os.getenv('AWS_PROFILE'), 'localstack')

    @mock.patch('requests.get')
    def test_full_process(self, mock_get):
        self.assert_using_localstack()
        [divisions_table, mps_table] = self.set_up_tables()
        self.set_mock_responses(mock_get)

        lambda_handler(None, None)

        saved_divisions = self.scan_table(divisions_table)['Items']
        self.assertEqual(len(saved_divisions), 2)

        division_ids = set(map(lambda x: int(x['DivisionId']), saved_divisions))
        self.assertEqual(division_ids, {-1, -2})

        saved_mps = self.scan_table(mps_table)['Items']
        for mp in saved_mps:
            self.assertEqual(len(mp['Votes']), 2)

        mps_as_map = {int(mp['MemberId']): mp for mp in saved_mps}
        self.assertEqual(len(mps_as_map), 6)
        self.assert_votes(mps_as_map[172]['Votes'], 'Aye', 'No', None)
        self.assert_votes(mps_as_map[4057]['Votes'], 'Aye', 'NoAttend', None)
        self.assert_votes(mps_as_map[39]['Votes'], 'Aye', 'Aye', None)
        self.assert_votes(mps_as_map[140]['Votes'], 'No', 'Aye', None)
        self.assert_votes(mps_as_map[4362]['Votes'], 'No', 'No', None)
        self.assert_votes(mps_as_map[4212]['Votes'], 'NoAttend', 'NoAttend', None)

        # second run
        lambda_handler(None, None)

        saved_divisions = self.scan_table(divisions_table)['Items']
        self.assertEqual(len(saved_divisions), 3)

        division_ids = set(map(lambda x: int(x['DivisionId']), saved_divisions))
        self.assertEqual(division_ids, {-1, -2, -3})

        saved_mps = self.scan_table(mps_table)['Items']
        for mp in saved_mps:
            self.assertEqual(len(mp['Votes']), 3)

        mps_as_map = {int(mp['MemberId']): mp for mp in saved_mps}
        self.assertEqual(len(mps_as_map), 6)
        self.assert_votes(mps_as_map[172]['Votes'], 'Aye', 'No', 'Aye')
        self.assert_votes(mps_as_map[4057]['Votes'], 'Aye', 'NoAttend', 'Aye')
        self.assert_votes(mps_as_map[39]['Votes'], 'Aye', 'Aye', 'Aye')
        self.assert_votes(mps_as_map[140]['Votes'], 'No', 'Aye', 'No')
        self.assert_votes(mps_as_map[4362]['Votes'], 'No', 'No', 'No')
        self.assert_votes(mps_as_map[4212]['Votes'], 'NoAttend', 'NoAttend', 'NoAttend')

        self.assert_queue()

    def assert_votes(self, mp_votes, first_vote, second_vote, third_vote):
        self.assertEqual(mp_votes[0]['Vote'], first_vote)
        self.assertEqual(mp_votes[1]['Vote'], second_vote)

        if (third_vote):
            self.assertEqual(mp_votes[2]['Vote'], third_vote)
            
    def assert_queue(self):
        today = date.today()
        year = today.year
        month = today.month

        sqs = self.get_sqs().Queue(localhost_queue_url)
        messages = sqs.receive_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].body, "Processed divisions for {month} {year}".format(month=month, year=year))

    def set_mock_responses(self, mock_get):
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


    def set_up_tables(self):
        self.delete_tables()
        [divisions_table, mps_table] = self.create_tables()
        self.load_mps(mps_table)
        return [divisions_table, mps_table]

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

    def get_sqs(self):
        if os.getenv('AWS_PROFILE') == 'localstack' and self.sqs is None:
            self.sqs = boto3.session.Session(profile_name='localstack').resource('sqs',
                                                                                      endpoint_url='http://localhost:4566')
        return self.sqs
