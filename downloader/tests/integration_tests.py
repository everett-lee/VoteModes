import json
import os
from unittest import TestCase, mock

import boto3

from downloader.tests.mock_response_helper.mock_response_helper import get_mock_response
from votesPerDivision.vote_per_division_downloader import get_mp_ids
from data import get_divisions
from downloader.main import run_download


@mock.patch.dict(os.environ, {'AWS_PROFILE': 'localstack'})
class IntegrationTests(TestCase):
    dynamodb = None

    def assert_using_localstack(self):
        self.assertEqual(os.getenv('AWS_PROFILE'), 'localstack')

    @mock.patch('requests.get')
    def test_full_process(self, mock_get):
        self.delete_tables()
        self.assert_using_localstack()
        [divisions_table, mps_table] = self.create_tables()

        mock_response_divisions = get_mock_response(status=200, text=json.dumps(get_divisions()))
        mock_response_empty = get_mock_response(status=200, text=json.dumps([]))

        mock_get.side_effect = [mock_response_divisions, mock_response_empty, mock_response_empty]
        run_download()

        divisions_items = self.scan_table(divisions_table)
        print(divisions_items)
        self.assertEqual(len(divisions_items['Items']), 2)

        # asser divisions szie equals ?
        # assert ids in divisions table

        # mp_ids = get_mp_ids()
        #
        # self.assertEqual(len(mp_ids), 647)
        #
        # for mp_id in mp_ids:
        #     self.assertIsInstance(mp_id, int)




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


    def delete_tables(self):
        divisions_table = self.get_dynamodb().Table('Divisions')
        mps_table = self.get_dynamodb().Table('Mps')

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