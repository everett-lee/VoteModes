import os
from typing import Union

import boto3

dynamodb_client = None
sqs_client = None


def get_dynamodb_client() -> Union[object, None]:
    AWS_PROFILE = os.getenv('AWS_PROFILE')
    invalid_profile_msg = 'Unable to get Boto client, AWS profile: {profile} is not valid'.format(profile=AWS_PROFILE)

    if AWS_PROFILE == 'localstack':
        dynamodb_client = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                                    endpoint_url='http://localhost:4566')

    elif AWS_PROFILE == 'votemodes':
        dynamodb_client = boto3.resource('dynamodb')

    else:
        raise RuntimeError(invalid_profile_msg)

    return dynamodb_client


def get_sqs_client() -> Union[object, None]:
    AWS_PROFILE = os.getenv('AWS_PROFILE')
    invalid_profile_msg = 'Unable to get Boto client, AWS profile: {profile} is not valid'.format(profile=AWS_PROFILE)

    if AWS_PROFILE == 'localstack':
        sqs_client = boto3.session.Session(profile_name='localstack').resource('sqs',
                                                                               endpoint_url='http://localhost:4566')

    elif AWS_PROFILE == 'votemodes':
        sqs_client = boto3.resource('sqs')

    else:
        raise RuntimeError(invalid_profile_msg)

    return sqs_client


def get_table(table_name: str) -> object:
    dynamodb = get_dynamodb_client()

    return dynamodb.Table(table_name)


def get_queue(queue_url: str) -> object:
    sqs = get_sqs_client()

    return sqs.Queue(queue_url)
