import os
from typing import Union

import boto3

dynamodb_client = None
sqs_client = None

def get_dynamodb_client() -> Union[object, None]:
    aws_profile = os.getenv('AWS_PROFILE')

    if aws_profile == 'localstack':
        dynamodb_client = boto3.session.Session(profile_name='localstack').resource('dynamodb',
                                                                                    endpoint_url='http://localhost:4566')
    else:
        dynamodb_client = boto3.resource('dynamodb')

    return dynamodb_client


def get_sqs_client() -> Union[object, None]:
    aws_profile = os.getenv('AWS_PROFILE')

    if aws_profile == 'localstack':
        sqs_client = boto3.session.Session(profile_name='localstack').resource('sqs',
                                                                               endpoint_url='http://localhost:4566')
    else:
        sqs_client = boto3.resource('sqs')

    return sqs_client


def get_table(table_name: str) -> object:
    dynamodb = dynamodb_client if dynamodb_client else get_dynamodb_client()

    return dynamodb.Table(table_name)


def get_queue(queue_url: str) -> object:
    sqs = sqs_client if sqs_client else get_sqs_client()

    return sqs.Queue(queue_url)
