import logging
import os
from typing import Union

import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_sqs import SQSServiceResource
from mypy_boto3_sqs.service_resource import Queue

DYNAMO_DB_CLIENT = None
SQS_CLIENT = None


def get_dynamodb_resource() -> Union[DynamoDBServiceResource, None]:
    global DYNAMO_DB_CLIENT
    if not DYNAMO_DB_CLIENT:
        logging.info("Creating DymamoDB client in local dev")
        if os.getenv("ENV") == "local-dev":
            DYNAMO_DB_CLIENT = boto3.resource(
                "dynamodb", endpoint_url="http://localhost:8000"
            )
        else:
            logging.info("Creating DynamoDB client")
            DYNAMO_DB_CLIENT = boto3.resource("dynamodb")

    return DYNAMO_DB_CLIENT


def get_sqs_client() -> Union[SQSServiceResource, None]:
    global SQS_CLIENT
    if not SQS_CLIENT:
        logging.info("Creating SQS client")
        SQS_CLIENT = boto3.resource("sqs")

    return SQS_CLIENT


def get_table(table_name: str) -> Table:
    dynamodb = get_dynamodb_resource()

    logging.info(f"Creating resource for table {table_name}")
    return dynamodb.Table(table_name)


def get_queue(queue_url: str) -> Queue:
    sqs = get_sqs_client()

    return sqs.Queue(url=queue_url)
