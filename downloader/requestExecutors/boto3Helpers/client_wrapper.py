import os
from typing import Union

import boto3

boto_client = None


def get_client() -> Union[object, None]:
    aws_profile = os.getenv('AWS_PROFILE')
    invalid_profile_msg = 'Unable to get Boto client, AWS profile: {profile} is not valid'.format(profile=aws_profile)

    if boto_client:
        return boto_client

    if aws_profile == 'localstack':
        dynamodb = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                             endpoint_url='http://localhost:4566')
    else:
        raise RuntimeError(invalid_profile_msg)

    return dynamodb


def get_table(table_name: str) -> object:
    dynamodb = get_client()

    return dynamodb.Table(table_name)
