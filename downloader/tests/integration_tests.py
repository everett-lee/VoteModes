import os
from unittest import TestCase, mock

from votesPerDivision.vote_per_division_downloader import get_mp_ids

@mock.patch.dict(os.environ, {'AWS_PROFILE': 'localstack'})
class IntegrationTests(TestCase):
    def assert_using_localstack(self):
        self.assertEqual(os.getenv('AWS_PROFILE'), 'localstack')

    def test_get_mp_ids(self):
        self.assert_using_localstack()

        mp_ids = get_mp_ids()

        self.assertEqual(len(mp_ids), 647)

        for mp_id in mp_ids:
            self.assertIsInstance(mp_id, int)
