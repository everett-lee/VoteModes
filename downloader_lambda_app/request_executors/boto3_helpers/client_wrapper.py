from typing import Union

import boto3

DYNAMO_DB_CLIENT = None
SQS_CLIENT = None


def get_dynamodb_client() -> Union[object, None]:
    global DYNAMO_DB_CLIENT
    DYNAMO_DB_CLIENT = boto3.resource("dynamodb")

    return DYNAMO_DB_CLIENT


def get_sqs_client() -> Union[object, None]:
    global SQS_CLIENT
    SQS_CLIENT = boto3.resource("sqs")

    return SQS_CLIENT


def get_table(table_name: str) -> object:
    global DYNAMO_DB_CLIENT
    dymnamo_db = DYNAMO_DB_CLIENT if DYNAMO_DB_CLIENT else get_dynamodb_client()

    return dymnamo_db.Table(table_name)


def get_queue(queue_url: str) -> object:
    global SQS_CLIENT
    sqs = SQS_CLIENT if SQS_CLIENT else get_sqs_client()

    return sqs.Queue(url=queue_url)
