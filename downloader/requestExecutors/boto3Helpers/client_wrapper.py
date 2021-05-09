import os
from typing import Union

import boto3

AWS_PROFILE = os.getenv('AWS_PROFILE')
INVALID_PROFILE_MSG = 'Unable to get Boto client, AWS profile: {profile} is not valid".format(profile=AWS_PROFILE)'
boto_client = None


def get_client() -> Union[object, None]:
    if boto_client:
        return boto_client

    if AWS_PROFILE == 'localstack':
        dynamodb = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                             endpoint_url='http://localhost:4566')
    else:
        raise RuntimeError(INVALID_PROFILE_MSG)

    return dynamodb


def get_table(table_name: str) -> object:
    dynamodb = get_client()

    return dynamodb.Table(table_name)
