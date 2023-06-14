import os
from typing import Union

import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_sqs import SQSServiceResource
from mypy_boto3_sqs.service_resource import Queue

DYNAMO_DB_RESOURCE = None
SQS_RESOURCE = None


def get_dynamodb_resource() -> DynamoDBServiceResource:
    global DYNAMO_DB_RESOURCE

    if not DYNAMO_DB_RESOURCE:
        if os.getenv("ENV") in ["local-dev"]:
            DYNAMO_DB_RESOURCE = boto3.resource(
                "dynamodb", endpoint_url="http://localhost:8000"
            )
        else:
            DYNAMO_DB_RESOURCE = boto3.resource("dynamodb")

    return DYNAMO_DB_RESOURCE


def get_sqs_resource() -> Union[SQSServiceResource, None]:
    global SQS_RESOURCE

    if not SQS_RESOURCE:
        SQS_RESOURCE = boto3.resource("sqs")

    return SQS_RESOURCE


def get_table(table_name: str) -> Table:
    dynamo_db = get_dynamodb_resource()

    return dynamo_db.Table(table_name)


def get_queue(queue_url: str) -> Queue:
    sqs = get_sqs_resource()

    return sqs.Queue(url=queue_url)
