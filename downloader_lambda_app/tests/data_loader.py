import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_divisions_first():
    with open(dir_path + "/data/first_divisions.json", "r") as file:
        return json.loads(file.read())


def get_divisions_second():
    with open(dir_path + "/data/second_divisions.json", "r") as file:
        return json.loads(file.read())


def get_divisions_third():
    with open(dir_path + "/data/third_divisions.json", "r") as file:
        return json.loads(file.read())


def get_mps():
    with open(dir_path + "/data/mps.json", "r") as file:
        return json.loads(file.read())


def get_divisions_with_votes_first():
    with open(dir_path + "/data/first_divisions_with_votes.json", "r") as file:
        return json.loads(file.read())


def get_divisions_with_votes_second():
    with open(dir_path + "/data/second_divisions_with_votes.json", "r") as file:
        return json.loads(file.read())


def get_divisions_with_votes_third():
    with open(dir_path + "/data/third_divisions_with_votes.json", "r") as file:
        return json.loads(file.read())
