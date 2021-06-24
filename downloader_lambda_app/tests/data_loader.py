import json


def get_divisions_first():
    with open('downloader_lambda_app/tests/data/first_divisions.json', 'r') as file:
        return json.loads(file.read())


def get_divisions_second():
    with open('downloader_lambda_app/tests/data/second_divisions.json', 'r') as file:
        return json.loads(file.read())


def get_mps():
    with open('downloader_lambda_app/tests/data/mps.json', 'r') as file:
        return json.loads(file.read())


def get_divisions_with_votes_first():
    with open('downloader_lambda_app/tests/data/first_divisions_with_votes.json', 'r') as file:
        return json.loads(file.read())


def get_divisions_with_votes_second():
    with open('downloader_lambda_app/tests/data/second_divisions_with_votes.json', 'r') as file:
        return json.loads(file.read())
